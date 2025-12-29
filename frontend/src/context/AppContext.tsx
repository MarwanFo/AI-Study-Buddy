import { createContext, useContext, useState, useCallback } from 'react';
import type { ReactNode } from 'react';
import type { Message, Document, SessionStats, SystemStatus } from '../types';
import { generateId } from '../lib/utils';

// API base URL - connects to Python backend
const API_BASE = 'http://localhost:8000';

interface AppContextType {
    // Documents
    documents: Document[];
    selectedDocument: string | null;
    isUploading: boolean;
    uploadDocument: (file: File) => Promise<void>;
    removeDocument: (name: string) => Promise<void>;
    selectDocument: (name: string | null) => void;

    // Chat
    messages: Message[];
    isLoading: boolean;
    sendMessage: (content: string) => Promise<void>;
    clearChat: () => void;

    // System
    systemStatus: SystemStatus;
    stats: SessionStats | null;
    checkSystem: () => Promise<void>;

    // UI
    sidebarOpen: boolean;
    toggleSidebar: () => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
    // Documents state
    const [documents, setDocuments] = useState<Document[]>([]);
    const [selectedDocument, setSelectedDocument] = useState<string | null>(null);
    const [isUploading, setIsUploading] = useState(false);

    // Chat state
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    // System state
    const [systemStatus, setSystemStatus] = useState<SystemStatus>({
        ollamaRunning: false,
        modelsReady: false,
        missingModels: [],
    });
    const [stats, setStats] = useState<SessionStats | null>(null);

    // UI state
    const [sidebarOpen, setSidebarOpen] = useState(true);

    // Check system status
    const checkSystem = useCallback(async () => {
        try {
            const res = await fetch(`${API_BASE}/status`);
            const data = await res.json();
            setSystemStatus({
                ollamaRunning: data.ollama_available,
                modelsReady: data.llm_ready && data.embedding_ready,
                missingModels: data.missing_models || [],
            });

            // Also fetch documents list
            const docsRes = await fetch(`${API_BASE}/documents`);
            const docsData = await docsRes.json();
            if (docsData.documents) {
                setDocuments(docsData.documents.map((name: string) => ({
                    id: generateId(),
                    name,
                    type: name.split('.').pop() || 'pdf',
                    chunks: 0,
                    pages: 0,
                    uploadedAt: new Date(),
                })));
            }

            // Fetch stats
            const statsRes = await fetch(`${API_BASE}/stats`);
            const statsData = await statsRes.json();
            setStats(statsData);
        } catch (error) {
            console.error('Failed to check system:', error);
            setSystemStatus({
                ollamaRunning: false,
                modelsReady: false,
                missingModels: ['Unable to connect to backend'],
            });
        }
    }, []);

    // Upload document
    const uploadDocument = useCallback(async (file: File) => {
        setIsUploading(true);
        try {
            const formData = new FormData();
            formData.append('file', file);

            const res = await fetch(`${API_BASE}/upload`, {
                method: 'POST',
                body: formData,
            });

            const data = await res.json();

            if (data.success) {
                const newDoc: Document = {
                    id: generateId(),
                    name: data.document_name,
                    type: data.file_type,
                    chunks: data.num_chunks,
                    pages: data.num_pages,
                    uploadedAt: new Date(),
                };
                setDocuments(prev => [...prev, newDoc]);
            } else {
                throw new Error(data.error || 'Failed to upload');
            }
        } finally {
            setIsUploading(false);
        }
    }, []);

    // Remove document
    const removeDocument = useCallback(async (name: string) => {
        try {
            await fetch(`${API_BASE}/documents/${encodeURIComponent(name)}`, {
                method: 'DELETE',
            });
            setDocuments(prev => prev.filter(d => d.name !== name));
            if (selectedDocument === name) {
                setSelectedDocument(null);
            }
        } catch (error) {
            console.error('Failed to remove document:', error);
        }
    }, [selectedDocument]);

    // Select document filter
    const selectDocument = useCallback((name: string | null) => {
        setSelectedDocument(name);
    }, []);

    // Send message
    const sendMessage = useCallback(async (content: string) => {
        // Add user message
        const userMessage: Message = {
            id: generateId(),
            role: 'user',
            content,
            timestamp: new Date(),
        };
        setMessages(prev => [...prev, userMessage]);

        // Add loading message
        const loadingMessage: Message = {
            id: generateId(),
            role: 'assistant',
            content: '',
            timestamp: new Date(),
            isLoading: true,
        };
        setMessages(prev => [...prev, loadingMessage]);
        setIsLoading(true);

        try {
            const res = await fetch(`${API_BASE}/ask`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: content,
                    document_filter: selectedDocument,
                }),
            });

            const data = await res.json();

            // Replace loading message with actual response
            const assistantMessage: Message = {
                id: loadingMessage.id,
                role: 'assistant',
                content: data.answer,
                sources: data.sources,
                timestamp: new Date(),
            };

            setMessages(prev => prev.map(m =>
                m.id === loadingMessage.id ? assistantMessage : m
            ));
        } catch (error) {
            // Replace loading message with error
            setMessages(prev => prev.map(m =>
                m.id === loadingMessage.id
                    ? { ...m, content: '❌ Failed to get response. Is the backend running?', isLoading: false }
                    : m
            ));
        } finally {
            setIsLoading(false);
        }
    }, [selectedDocument]);

    // Clear chat
    const clearChat = useCallback(() => {
        setMessages([]);
        fetch(`${API_BASE}/clear-chat`, { method: 'POST' }).catch(console.error);
    }, []);

    // Toggle sidebar
    const toggleSidebar = useCallback(() => {
        setSidebarOpen(prev => !prev);
    }, []);

    return (
        <AppContext.Provider
            value={{
                documents,
                selectedDocument,
                isUploading,
                uploadDocument,
                removeDocument,
                selectDocument,
                messages,
                isLoading,
                sendMessage,
                clearChat,
                systemStatus,
                stats,
                checkSystem,
                sidebarOpen,
                toggleSidebar,
            }}
        >
            {children}
        </AppContext.Provider>
    );
}

export function useApp() {
    const context = useContext(AppContext);
    if (context === undefined) {
        throw new Error('useApp must be used within an AppProvider');
    }
    return context;
}
