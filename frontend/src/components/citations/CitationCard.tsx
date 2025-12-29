import { motion } from 'framer-motion';
import { FileText } from 'lucide-react';
import type { Source } from '../../types';
import Badge from '../ui/Badge';
import { truncate } from '../../lib/utils';

interface CitationCardProps {
    source: Source;
    index: number;
}

export function CitationCard({ source, index }: CitationCardProps) {
    // Color based on relevance
    const relevanceVariant = source.relevance >= 80
        ? 'success'
        : source.relevance >= 60
            ? 'warning'
            : 'default';

    return (
        <motion.div
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-stone-50 rounded-xl p-4 border border-stone-100"
        >
            {/* Header */}
            <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                    <div className="w-6 h-6 rounded-md bg-amber-100 flex items-center justify-center">
                        <FileText className="w-3.5 h-3.5 text-amber-600" />
                    </div>
                    <span className="text-sm font-medium text-stone-700">
                        {truncate(source.document, 25)}
                    </span>
                </div>

                <div className="flex items-center gap-2">
                    <Badge variant="primary" size="sm">
                        Page {source.page}
                    </Badge>
                    <Badge variant={relevanceVariant} size="sm">
                        {source.relevance}%
                    </Badge>
                </div>
            </div>

            {/* Content */}
            <p className="text-sm text-stone-600 leading-relaxed">
                {source.content}
            </p>
        </motion.div>
    );
}

export default CitationCard;
