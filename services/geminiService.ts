
import { GoogleGenAI, Modality } from "@google/genai";
import type { ImageFile, GenerationResult, StyleRequest } from '../types';
import { getHairstyleById } from '../constants/hairstyles';

const PROMPT = `Based on the two images provided, please perform a realistic virtual try-on.
The first image is of a person. The second image contains a style item (hairstyle, clothing, accessory, etc.).
Your task is to edit the first image to show the person wearing or using the item from the second image.
The final image should be a high-quality, realistic visualization. If you have any comments, provide them in the text part.`;

export const generateVirtualTryOn = async (
  personImage: ImageFile,
  styleRequest: StyleRequest
): Promise<GenerationResult> => {
  if (!import.meta.env.VITE_API_KEY) {
    throw new Error("VITE_API_KEY environment variable is not set.");
  }
  
  const ai = new GoogleGenAI({ apiKey: import.meta.env.VITE_API_KEY });

  // Build the prompt based on style request type
  let prompt: string;
  let parts: any[] = [
    {
      inlineData: {
        data: personImage.base64,
        mimeType: personImage.mimeType,
      },
    }
  ];

  if (styleRequest.type === 'image' && styleRequest.image) {
    // Image-based style request
    prompt = PROMPT;
    parts.push({
      inlineData: {
        data: styleRequest.image.base64,
        mimeType: styleRequest.image.mimeType,
      },
    });
  } else if (styleRequest.type === 'text') {
    // Text-based style request
    let stylePrompt = styleRequest.text || '';
    
    // If it's a preset, use the optimized prompt
    if (styleRequest.presetId) {
      const preset = getHairstyleById(styleRequest.presetId);
      if (preset) {
        stylePrompt = preset.prompt;
      }
    }
    
    prompt = `Based on the person's image provided, please apply the following style: "${stylePrompt}". 
    This could be a hairstyle, clothing item, accessory (like glasses, earrings, hat, etc.), or any other style element.
    The final image should be a high-quality, realistic visualization of the person with the new style applied. 
    Maintain the person's facial features and skin tone while applying the requested style. 
    If you have any comments about the transformation, provide them in the text part.`;
  } else {
    throw new Error("Invalid style request: must provide either an image or text description.");
  }

  parts.push({ text: prompt });

  const response = await ai.models.generateContent({
    model: 'gemini-2.5-flash-image-preview',
    contents: { parts },
    config: {
      responseModalities: [Modality.IMAGE, Modality.TEXT],
    },
  });

  let generatedImageUrl = '';
  let generatedText = 'No text was generated.';

  if (response.candidates && response.candidates.length > 0) {
    for (const part of response.candidates[0].content.parts) {
      if (part.inlineData) {
        const base64ImageBytes: string = part.inlineData.data;
        generatedImageUrl = `data:${part.inlineData.mimeType};base64,${base64ImageBytes}`;
      } else if (part.text) {
        generatedText = part.text;
      }
    }
  }

  if (!generatedImageUrl) {
    throw new Error("API did not return an image. The response might have been blocked.");
  }

  return { imageUrl: generatedImageUrl, text: generatedText };
};
