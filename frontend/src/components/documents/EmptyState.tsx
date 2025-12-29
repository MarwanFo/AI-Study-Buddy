import { motion } from 'framer-motion';
import { FileText, Sparkles } from 'lucide-react';

export function EmptyState() {
    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="px-4 py-8 text-center"
        >
            <div className="relative inline-block mb-4">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-amber-100 to-orange-100 flex items-center justify-center">
                    <FileText className="w-8 h-8 text-amber-500" />
                </div>
                <motion.div
                    animate={{
                        scale: [1, 1.2, 1],
                        rotate: [0, 10, -10, 0],
                    }}
                    transition={{
                        duration: 2,
                        repeat: Infinity,
                        repeatDelay: 3,
                    }}
                    className="absolute -top-1 -right-1 w-6 h-6 rounded-full bg-amber-500 flex items-center justify-center"
                >
                    <Sparkles className="w-3 h-3 text-white" />
                </motion.div>
            </div>

            <h3 className="text-base font-semibold text-stone-700 mb-1">
                No documents yet
            </h3>
            <p className="text-sm text-stone-500 max-w-[200px] mx-auto">
                Upload your study materials to get started with AI-powered learning
            </p>
        </motion.div>
    );
}

export default EmptyState;
