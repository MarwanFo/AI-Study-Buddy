import type { ReactNode } from 'react';
import { motion } from 'framer-motion';
import { cn } from '../../lib/utils';

interface CardProps {
    children: ReactNode;
    className?: string;
    hover?: boolean;
    onClick?: () => void;
}

export function Card({ children, className, hover = false, onClick }: CardProps) {
    const Component = hover ? motion.div : 'div';

    return (
        <Component
            className={cn(
                `bg-white rounded-2xl border border-stone-200
        shadow-sm`,
                hover && 'cursor-pointer transition-all duration-200 hover:shadow-md hover:border-stone-300',
                onClick && 'cursor-pointer',
                className
            )}
            onClick={onClick}
            {...(hover && {
                whileHover: { y: -2 },
                whileTap: { scale: 0.98 },
            })}
        >
            {children}
        </Component>
    );
}

interface CardHeaderProps {
    children: ReactNode;
    className?: string;
}

export function CardHeader({ children, className }: CardHeaderProps) {
    return (
        <div className={cn('px-5 py-4 border-b border-stone-100', className)}>
            {children}
        </div>
    );
}

interface CardContentProps {
    children: ReactNode;
    className?: string;
}

export function CardContent({ children, className }: CardContentProps) {
    return (
        <div className={cn('px-5 py-4', className)}>
            {children}
        </div>
    );
}

interface CardFooterProps {
    children: ReactNode;
    className?: string;
}

export function CardFooter({ children, className }: CardFooterProps) {
    return (
        <div className={cn('px-5 py-4 border-t border-stone-100', className)}>
            {children}
        </div>
    );
}

export default Card;
