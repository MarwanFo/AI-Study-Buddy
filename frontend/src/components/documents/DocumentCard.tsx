import { motion } from 'framer-motion';
import { FileText, X } from 'lucide-react';
import type { Document } from '../../types';
import { useApp } from '../../context/AppContext';
import { cn, getFileTypeLabel, truncate } from '../../lib/utils';
import Badge from '../ui/Badge';

interface DocumentCardProps {
    document: Document;
}

export function DocumentCard({ document }: DocumentCardProps) {
    const { removeDocument, selectedDocument, selectDocument } = useApp();
    const isSelected = selectedDocument === document.name;

    return (
        <motion.div
            layout
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            whileHover={{ x: 4 }}
            className={cn(
                `group relative flex items-start gap-3 p-3 rounded-xl
        transition-colors duration-200 cursor-pointer`,
                isSelected
                    ? 'bg-amber-50 border border-amber-200'
                    : 'hover:bg-stone-50 border border-transparent'
            )}
            onClick={() => selectDocument(isSelected ? null : document.name)}
        >
            {/* Icon */}
            <div className={cn(
                'flex-shrink-0 w-9 h-9 rounded-lg flex items-center justify-center',
                isSelected ? 'bg-amber-100' : 'bg-stone-100 group-hover:bg-stone-200'
            )}>
                <FileText className={cn(
                    'w-5 h-5',
                    isSelected ? 'text-amber-600' : 'text-stone-400'
                )} />
            </div>

            {/* Content */}
            <div className="flex-1 min-w-0">
                <p className={cn(
                    'text-sm font-medium truncate',
                    isSelected ? 'text-amber-700' : 'text-stone-700'
                )}>
                    {truncate(document.name, 22)}
                </p>
                <div className="flex items-center gap-2 mt-1">
                    <Badge variant={isSelected ? 'primary' : 'default'} size="sm">
                        {getFileTypeLabel(document.name)}
                    </Badge>
                    {document.chunks > 0 && (
                        <span className="text-xs text-stone-400">
                            {document.chunks} chunks
                        </span>
                    )}
                </div>
            </div>

            {/* Delete button */}
            <button
                onClick={(e) => {
                    e.stopPropagation();
                    removeDocument(document.name);
                }}
                className={cn(
                    `absolute right-2 top-2 p-1.5 rounded-lg
          opacity-0 group-hover:opacity-100
          transition-all duration-200
          hover:bg-red-100 text-stone-400 hover:text-red-600`
                )}
            >
                <X className="w-4 h-4" />
            </button>
        </motion.div>
    );
}

export default DocumentCard;
