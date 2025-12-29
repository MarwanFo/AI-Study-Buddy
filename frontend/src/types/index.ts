// Core type definitions for the Study Buddy app

export interface Document {
    id: string;
    name: string;
    type: 'pdf' | 'docx' | 'txt' | 'md';
    chunks: number;
    pages: number;
    uploadedAt: Date;
}

export interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    sources?: Source[];
    timestamp: Date;
    isLoading?: boolean;
}

export interface Source {
    document: string;
    page: number;
    content: string;
    relevance: number;
}

export interface ChatState {
    messages: Message[];
    isLoading: boolean;
    error: string | null;
}

export interface DocumentState {
    documents: Document[];
    selectedDocument: string | null;
    isUploading: boolean;
    uploadProgress: number;
    error: string | null;
}

export interface AppState {
    chat: ChatState;
    documents: DocumentState;
    sidebarOpen: boolean;
    systemStatus: SystemStatus;
}

export interface SystemStatus {
    ollamaRunning: boolean;
    modelsReady: boolean;
    missingModels: string[];
}

export interface ApiResponse<T> {
    success: boolean;
    data?: T;
    error?: string;
}

export interface AskQuestionResponse {
    answer: string;
    sources: Source[];
    documents_searched: string[];
    error: string | null;
}

export interface ProcessDocumentResponse {
    success: boolean;
    document_name: string;
    file_type: string;
    total_characters: number;
    num_chunks: number;
    num_pages: number;
    total_documents: number;
}

export interface SessionStats {
    questions_asked: number;
    chunks_retrieved: number;
    documents_processed: number;
    conversation_length: number;
    documents_loaded: number;
    total_chunks: number;
}
