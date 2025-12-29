import { motion } from 'framer-motion';
import { User, Bot } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import type { Message } from '../../types';
import { cn, formatRelativeTime } from '../../lib/utils';
import CitationList from '../citations/CitationList';
import TypingIndicator from './TypingIndicator';

interface ChatMessageProps {
    message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
    const isUser = message.role === 'user';

    return (
        <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ duration: 0.3, ease: 'easeOut' }}
            className={cn(
                'flex gap-3 max-w-[85%]',
                isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'
            )}
        >
            {/* Avatar */}
            <div className={cn(
                'flex-shrink-0 w-9 h-9 rounded-xl flex items-center justify-center',
                isUser
                    ? 'bg-amber-500 shadow-lg'
                    : 'bg-stone-100 border border-stone-200'
            )}>
                {isUser ? (
                    <User className="w-5 h-5 text-white" />
                ) : (
                    <Bot className="w-5 h-5 text-amber-600" />
                )}
            </div>

            {/* Message content */}
            <div className="flex flex-col gap-1">
                <div className={cn(
                    'px-4 py-3 rounded-2xl',
                    isUser
                        ? 'bg-amber-500 text-white rounded-tr-sm'
                        : 'bg-white border border-stone-200 rounded-tl-sm shadow-sm'
                )}>
                    {message.isLoading ? (
                        <TypingIndicator />
                    ) : (
                        <div className={cn(
                            'text-sm leading-relaxed prose prose-sm max-w-none',
                            isUser ? 'text-white prose-invert' : 'text-stone-700'
                        )}>
                            <ReactMarkdown>
                                {message.content}
                            </ReactMarkdown>
                        </div>
                    )}
                </div>

                {/* Timestamp */}
                <span className={cn(
                    'text-xs text-stone-400 px-1',
                    isUser ? 'text-right' : 'text-left'
                )}>
                    {formatRelativeTime(message.timestamp)}
                </span>

                {/* Sources */}
                {!isUser && message.sources && message.sources.length > 0 && (
                    <CitationList sources={message.sources} />
                )}
            </div>
        </motion.div>
    );
}

export default ChatMessage;
