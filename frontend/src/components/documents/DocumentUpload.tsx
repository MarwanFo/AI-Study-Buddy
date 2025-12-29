import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileText, Loader2 } from 'lucide-react';
import { useApp } from '../../context/AppContext';
import { cn } from '../../lib/utils';

export function DocumentUpload() {
    const { uploadDocument, isUploading } = useApp();

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        for (const file of acceptedFiles) {
            await uploadDocument(file);
        }
    }, [uploadDocument]);

    const { getRootProps, getInputProps, isDragActive, isDragAccept } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
            'text/plain': ['.txt'],
            'text/markdown': ['.md'],
        },
        disabled: isUploading,
    });

    // Extract only the props we need from dropzone to avoid type conflicts
    const rootProps = getRootProps();
    const { onClick, onKeyDown, role, tabIndex } = rootProps;

    return (
        <div className="p-4">
            <motion.div
                onClick={onClick}
                onKeyDown={onKeyDown}
                role={role}
                tabIndex={tabIndex}
                className={cn(
                    `relative rounded-2xl border-2 border-dashed p-6
          transition-all duration-300 cursor-pointer
          flex flex-col items-center justify-center text-center`,
                    isDragActive
                        ? 'border-amber-500 bg-amber-50 scale-[1.02]'
                        : 'border-stone-300 bg-stone-50 hover:border-amber-400 hover:bg-amber-50/50',
                    isDragAccept && 'border-green-500 bg-green-50',
                    isUploading && 'opacity-50 cursor-not-allowed'
                )}
                whileHover={{ scale: isUploading ? 1 : 1.01 }}
                whileTap={{ scale: isUploading ? 1 : 0.99 }}
            >
                <input {...getInputProps()} />

                <AnimatePresence mode="wait">
                    {isUploading ? (
                        <motion.div
                            key="loading"
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.8 }}
                            className="flex flex-col items-center"
                        >
                            <Loader2 className="w-10 h-10 text-amber-500 animate-spin mb-3" />
                            <p className="text-sm font-medium text-stone-600">
                                Processing document...
                            </p>
                        </motion.div>
                    ) : isDragActive ? (
                        <motion.div
                            key="drag"
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.8 }}
                            className="flex flex-col items-center"
                        >
                            <FileText className="w-10 h-10 text-amber-500 mb-3" />
                            <p className="text-sm font-medium text-amber-600">
                                Drop to upload!
                            </p>
                        </motion.div>
                    ) : (
                        <motion.div
                            key="default"
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.8 }}
                            className="flex flex-col items-center"
                        >
                            <div className="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center mb-3">
                                <Upload className="w-6 h-6 text-amber-600" />
                            </div>
                            <p className="text-sm font-medium text-stone-700 mb-1">
                                Drop files or click to browse
                            </p>
                            <p className="text-xs text-stone-500">
                                PDF, DOCX, TXT, MD
                            </p>
                        </motion.div>
                    )}
                </AnimatePresence>
            </motion.div>
        </div>
    );
}

export default DocumentUpload;
