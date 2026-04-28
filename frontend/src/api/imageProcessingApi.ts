import axiosClient from "./axiosClient";
import type {
  ImageFilterName,
  ImageProcessingResponse,
} from "../types/imageProcessingTypes";

interface ProcessImageParams {
  imageFile: File;
  filterName: ImageFilterName;
  kernelSize: number;
  sigmaValue: number;
}

export async function processImage(
  params: ProcessImageParams,
): Promise<ImageProcessingResponse> {
  const formData = new FormData();

  formData.append("upload_file", params.imageFile);
  formData.append("filter_name", params.filterName);
  formData.append("kernel_size", String(params.kernelSize));
  formData.append("sigma_value", String(params.sigmaValue));

  const response = await axiosClient.post<ImageProcessingResponse>(
    "/api/v1/image-processing/enhance",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    },
  );

  return response.data;
}
