import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, BookOpen } from 'lucide-react';
import type { Source } from '../../types';
import CitationCard from './CitationCard';
import { cn } from '../../lib/utils';

interface CitationListProps {
    sources: Source[];
}

export function CitationList({ sources }: CitationListProps) {
    const [isOpen, setIsOpen] = useState(false);

    if (sources.length === 0) return null;

    return (
        <div className="mt-2">
            <motion.button
                onClick={() => setIsOpen(!isOpen)}
                className={cn(
                    `flex items-center gap-2 px-3 py-1.5 rounded-lg
          text-sm font-medium transition-colors`,
                    isOpen
                        ? 'text-amber-600 bg-amber-50'
                        : 'text-stone-500 hover:text-amber-600 hover:bg-amber-50/50'
                )}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
            >
                <BookOpen className="w-4 h-4" />
                <span>View sources ({sources.length})</span>
                <motion.div
                    animate={{ rotate: isOpen ? 180 : 0 }}
                    transition={{ duration: 0.2 }}
                >
                    <ChevronDown className="w-4 h-4" />
                </motion.div>
            </motion.button>

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.2 }}
                        className="overflow-hidden"
                    >
                        <div className="mt-3 space-y-2">
                            {sources.map((source, idx) => (
                                <CitationCard key={idx} source={source} index={idx + 1} />
                            ))}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

export default CitationList;
