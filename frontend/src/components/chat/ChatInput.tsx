import { useState, useRef, useEffect } from 'react';
import type { KeyboardEvent } from 'react';
import { motion } from 'framer-motion';
import { Send, Sparkles } from 'lucide-react';
import { useApp } from '../../context/AppContext';
import { cn } from '../../lib/utils';

export function ChatInput() {
    const [input, setInput] = useState('');
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const { sendMessage, isLoading, documents } = useApp();

    const hasDocuments = documents.length > 0;
    const canSend = input.trim() && hasDocuments && !isLoading;

    // Auto-resize textarea
    useEffect(() => {
        const textarea = textareaRef.current;
        if (textarea) {
            textarea.style.height = 'auto';
            textarea.style.height = `${Math.min(textarea.scrollHeight, 150)}px`;
        }
    }, [input]);

    const handleSubmit = () => {
        if (canSend) {
            sendMessage(input.trim());
            setInput('');
        }
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="sticky bottom-0 bg-gradient-to-t from-stone-50 via-stone-50 to-stone-50/80 pt-4 pb-6 px-6"
        >
            <div className={cn(
                `relative flex items-end gap-3 bg-white rounded-2xl 
        border border-stone-200 shadow-lg
        transition-all duration-200`,
                !hasDocuments && 'opacity-50'
            )}>
                {/* Sparkle decoration */}
                <div className="absolute -top-2 -left-2">
                    <motion.div
                        animate={{ rotate: [0, 15, -15, 0] }}
                        transition={{ duration: 4, repeat: Infinity }}
                    >
                        <Sparkles className="w-5 h-5 text-amber-400" />
                    </motion.div>
                </div>

                {/* Textarea */}
                <textarea
                    ref={textareaRef}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder={
                        hasDocuments
                            ? "Ask anything about your documents..."
                            : "Upload a document first to ask questions"
                    }
                    disabled={!hasDocuments || isLoading}
                    rows={1}
                    className={cn(
                        `flex-1 py-4 pl-5 pr-14 bg-transparent
            text-stone-800 placeholder:text-stone-400
            resize-none outline-none
            text-sm leading-relaxed`,
                        isLoading && 'opacity-50'
                    )}
                />

                {/* Send button */}
                <motion.button
                    onClick={handleSubmit}
                    disabled={!canSend}
                    whileHover={{ scale: canSend ? 1.05 : 1 }}
                    whileTap={{ scale: canSend ? 0.95 : 1 }}
                    className={cn(
                        `absolute right-3 bottom-3 p-2.5 rounded-xl
            transition-all duration-200`,
                        canSend
                            ? 'bg-amber-500 text-white shadow-lg hover:bg-amber-600'
                            : 'bg-stone-100 text-stone-400 cursor-not-allowed'
                    )}
                >
                    <Send className="w-5 h-5" />
                </motion.button>
            </div>

            {/* Hint */}
            <p className="text-xs text-stone-400 text-center mt-3">
                Press <kbd className="px-1.5 py-0.5 bg-stone-100 rounded text-stone-500 font-mono">Enter</kbd> to send • <kbd className="px-1.5 py-0.5 bg-stone-100 rounded text-stone-500 font-mono">Shift+Enter</kbd> for new line
            </p>
        </motion.div>
    );
}

export default ChatInput;
