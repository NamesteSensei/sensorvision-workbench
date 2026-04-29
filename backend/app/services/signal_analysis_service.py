"""Signal analysis service using pandas, NumPy, SciPy, and matplotlib."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fastapi import HTTPException, UploadFile, status
from scipy.fft import fft, fftfreq

from app.core.constants import SIGNAL_OUTPUT_DIR
from app.schemas.signal_analysis import (
    SignalAnalysisOptions,
    SignalAnalysisResponse,
)
from app.services.file_service import FileService
from app.services.storage_service import StorageService


class SignalAnalysisService:
    """Service responsible for signal processing operations."""

    def __init__(self) -> None:
        """Initialize signal analysis service dependencies."""
        self.file_service = FileService()
        self.storage_service = StorageService()

    async def analyze_uploaded_signal(
        self,
        upload_file: UploadFile,
        options: SignalAnalysisOptions,
    ) -> SignalAnalysisResponse:
        """Validate, save, analyze, and plot an uploaded CSV signal."""
        upload_response = await self.file_service.save_validated_upload(
            upload_file=upload_file,
            file_category="signal",
        )

        input_path = (
            self.storage_service.get_input_directory("signal")
            / upload_response.stored_file_name
        )

        data_frame = self._read_signal_csv(input_path)
        signal_values = self._get_signal_column(
            data_frame=data_frame,
            selected_column=options.selected_column,
        )

        smoothed_signal = self._smooth_signal(
            signal_values=signal_values,
            smoothing_window=options.smoothing_window,
        )

        frequency_values, magnitude_values = self._compute_fft(
            signal_values=smoothed_signal,
            sampling_rate_hz=options.sampling_rate_hz,
        )

        SIGNAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        time_plot_path = SIGNAL_OUTPUT_DIR / (
            f"{upload_response.job_id}_time_domain.png"
        )
        frequency_plot_path = SIGNAL_OUTPUT_DIR / (
            f"{upload_response.job_id}_frequency_domain.png"
        )

        self._save_time_domain_plot(
            signal_values=signal_values,
            smoothed_signal=smoothed_signal,
            output_path=time_plot_path,
        )

        self._save_frequency_domain_plot(
            frequency_values=frequency_values,
            magnitude_values=magnitude_values,
            output_path=frequency_plot_path,
        )

        return SignalAnalysisResponse(
            job_id=upload_response.job_id,
            original_file_name=upload_response.original_file_name,
            stored_file_name=upload_response.stored_file_name,
            file_category="signal",
            selected_column=options.selected_column,
            sample_count=len(signal_values),
            sampling_rate_hz=options.sampling_rate_hz,
            smoothing_window=options.smoothing_window,
            time_plot_url=self.storage_service.build_file_url(time_plot_path),
            frequency_plot_url=self.storage_service.build_file_url(
                frequency_plot_path,
            ),
            file_size_bytes=upload_response.file_size_bytes,
            message="Signal analysis completed successfully.",
        )

    def _read_signal_csv(self, input_path: Path) -> pd.DataFrame:
        """Read signal data from a CSV file."""
        try:
            data_frame = pd.read_csv(input_path)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CSV file could not be read.",
            ) from error

        if data_frame.empty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CSV file is empty.",
            )

        return data_frame

    def _get_signal_column(
        self,
        data_frame: pd.DataFrame,
        selected_column: str,
    ) -> np.ndarray:
        """Extract and validate a numeric signal column."""
        if selected_column not in data_frame.columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Column '{selected_column}' was not found in CSV.",
            )

        signal_series = pd.to_numeric(
            data_frame[selected_column],
            errors="coerce",
        ).dropna()

        if signal_series.empty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Column '{selected_column}' has no numeric values.",
            )

        return signal_series.to_numpy(dtype=float)

    def _smooth_signal(
        self,
        signal_values: np.ndarray,
        smoothing_window: int,
    ) -> np.ndarray:
        """Apply moving average smoothing to a signal."""
        if smoothing_window <= 1:
            return signal_values

        if smoothing_window > len(signal_values):
            smoothing_window = len(signal_values)

        kernel = np.ones(smoothing_window) / smoothing_window
        return np.convolve(signal_values, kernel, mode="same")

    def _compute_fft(
        self,
        signal_values: np.ndarray,
        sampling_rate_hz: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Compute one-sided FFT frequency and magnitude values."""
        sample_count = len(signal_values)

        if sample_count < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least two signal samples are required for FFT.",
            )

        centered_signal = signal_values - np.mean(signal_values)
        fft_values = fft(centered_signal)
        frequency_values = fftfreq(sample_count, d=1.0 / sampling_rate_hz)

        positive_frequency_mask = frequency_values >= 0

        return (
            frequency_values[positive_frequency_mask],
            np.abs(fft_values[positive_frequency_mask]),
        )

    def _save_time_domain_plot(
        self,
        signal_values: np.ndarray,
        smoothed_signal: np.ndarray,
        output_path: Path,
    ) -> None:
        """Save original and smoothed signal time-domain plot."""
        plt.figure(figsize=(10, 5))
        plt.plot(signal_values, label="Original Signal")
        plt.plot(smoothed_signal, label="Smoothed Signal")
        plt.title("Time Domain Signal")
        plt.xlabel("Sample Index")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def _save_frequency_domain_plot(
        self,
        frequency_values: np.ndarray,
        magnitude_values: np.ndarray,
        output_path: Path,
    ) -> None:
        """Save signal frequency-domain magnitude plot."""
        plt.figure(figsize=(10, 5))
        plt.plot(frequency_values, magnitude_values)
        plt.title("Frequency Domain Magnitude")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
