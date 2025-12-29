import { useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageCircle, Trash2 } from 'lucide-react';
import { useApp } from '../../context/AppContext';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import Button from '../ui/Button';

export function ChatContainer() {
    const { messages, clearChat, documents, selectedDocument } = useApp();
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Auto-scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const hasMessages = messages.length > 0;
    const hasDocuments = documents.length > 0;

    return (
        <div className="flex flex-col h-full">
            {/* Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-stone-100">
                <div>
                    <h2 className="text-lg font-semibold text-stone-800">
                        Chat
                    </h2>
                    {selectedDocument && (
                        <p className="text-xs text-amber-600 mt-0.5">
                            Filtering: {selectedDocument}
                        </p>
                    )}
                </div>

                {hasMessages && (
                    <Button
                        variant="ghost"
                        size="sm"
                        onClick={clearChat}
                        leftIcon={<Trash2 className="w-4 h-4" />}
                    >
                        Clear
                    </Button>
                )}
            </div>

            {/* Messages area */}
            <div className="flex-1 overflow-y-auto px-6 py-6">
                {hasMessages ? (
                    <div className="space-y-6">
                        <AnimatePresence mode="popLayout">
                            {messages.map((message) => (
                                <ChatMessage key={message.id} message={message} />
                            ))}
                        </AnimatePresence>
                        <div ref={messagesEndRef} />
                    </div>
                ) : (
                    <EmptyChatState hasDocuments={hasDocuments} />
                )}
            </div>

            {/* Input */}
            <ChatInput />
        </div>
    );
}

function EmptyChatState({ hasDocuments }: { hasDocuments: boolean }) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col items-center justify-center h-full text-center px-8"
        >
            <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-amber-100 to-orange-100 flex items-center justify-center mb-6 shadow-sm">
                <MessageCircle className="w-10 h-10 text-amber-500" />
            </div>

            <h3 className="text-xl font-semibold text-stone-800 mb-2">
                {hasDocuments ? "Ready to help you study!" : "No documents yet"}
            </h3>

            <p className="text-stone-500 max-w-sm leading-relaxed">
                {hasDocuments
                    ? "Ask me anything about your uploaded documents. I'll find the relevant information and cite my sources."
                    : "Upload some study materials in the sidebar to get started with AI-powered learning."
                }
            </p>

            {hasDocuments && (
                <div className="mt-8 space-y-2">
                    <p className="text-xs text-stone-400 uppercase tracking-wider font-medium">
                        Try asking
                    </p>
                    <div className="flex flex-wrap gap-2 justify-center">
                        {[
                            "What is this about?",
                            "Summarize the key points",
                            "Explain in simple terms",
                        ].map((suggestion) => (
                            <motion.button
                                key={suggestion}
                                whileHover={{ scale: 1.02 }}
                                whileTap={{ scale: 0.98 }}
                                className="px-4 py-2 text-sm bg-white hover:bg-stone-50 text-stone-600 rounded-full border border-stone-200 transition-colors shadow-sm"
                            >
                                {suggestion}
                            </motion.button>
                        ))}
                    </div>
                </div>
            )}
        </motion.div>
    );
}

export default ChatContainer;
