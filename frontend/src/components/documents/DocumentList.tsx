import { AnimatePresence } from 'framer-motion';
import { useApp } from '../../context/AppContext';
import DocumentCard from './DocumentCard';
import EmptyState from './EmptyState';

export function DocumentList() {
    const { documents } = useApp();

    if (documents.length === 0) {
        return <EmptyState />;
    }

    return (
        <div className="px-3 py-2 space-y-1">
            <div className="px-1 mb-2">
                <h3 className="text-xs font-semibold text-text-tertiary uppercase tracking-wider">
                    Your Documents
                </h3>
            </div>

            <AnimatePresence mode="popLayout">
                {documents.map((doc) => (
                    <DocumentCard key={doc.id} document={doc} />
                ))}
            </AnimatePresence>
        </div>
    );
}

export default DocumentList;
