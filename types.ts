
export interface ImageFile {
  base64: string;
  mimeType: string;
}

export interface StyleRequest {
  type: 'image' | 'text';
  image?: ImageFile;
  text?: string;
  presetId?: string;
}

export interface GenerationResult {
  imageUrl: string;
  text: string;
}
