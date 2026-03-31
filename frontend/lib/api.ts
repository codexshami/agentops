import axios, { AxiosInstance } from "axios";
import { ChatRequest, ChatResponse, Conversation } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }

  async healthCheck() {
    try {
      const response = await this.client.get("/health");
      return response.data;
    } catch (error) {
      throw new Error("Failed to connect to backend");
    }
  }

  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await this.client.post("/api/chat/send", request);
    return response.data;
  }

  async generateCode(prompt: string) {
    const response = await this.client.post("/api/chat/generate-code", {
      message: prompt,
    });
    return response.data;
  }

  async getConversations(): Promise<Conversation[]> {
    const response = await this.client.get("/api/conversations/");
    return response.data;
  }

  async getConversation(id: string): Promise<Conversation> {
    const response = await this.client.get(`/api/conversations/${id}`);
    return response.data;
  }

  async createConversation(): Promise<Conversation> {
    const response = await this.client.post("/api/conversations/create");
    return response.data;
  }
}

export const apiClient = new APIClient();