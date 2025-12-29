import { motion } from 'framer-motion';

export function TypingIndicator() {
    return (
        <div className="flex items-center gap-1 py-1">
            {[0, 1, 2].map((i) => (
                <motion.span
                    key={i}
                    className="w-2 h-2 bg-stone-400 rounded-full"
                    animate={{
                        opacity: [0.4, 1, 0.4],
                        scale: [0.8, 1, 0.8],
                    }}
                    transition={{
                        duration: 1,
                        repeat: Infinity,
                        delay: i * 0.2,
                        ease: 'easeInOut',
                    }}
                />
            ))}
        </div>
    );
}

export default TypingIndicator;
