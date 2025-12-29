import { forwardRef } from 'react';
import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';
import { cn } from '../../lib/utils';

interface ButtonProps {
    variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
    size?: 'sm' | 'md' | 'lg';
    isLoading?: boolean;
    leftIcon?: React.ReactNode;
    rightIcon?: React.ReactNode;
    disabled?: boolean;
    className?: string;
    children?: React.ReactNode;
    onClick?: () => void;
    type?: 'button' | 'submit' | 'reset';
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
    (
        {
            className,
            variant = 'primary',
            size = 'md',
            isLoading = false,
            leftIcon,
            rightIcon,
            disabled,
            children,
            onClick,
            type = 'button',
        },
        ref
    ) => {
        const baseStyles = `
      inline-flex items-center justify-center
      font-medium rounded-xl
      transition-all duration-200
      focus:outline-none focus:ring-2 focus:ring-offset-2
      disabled:opacity-50 disabled:cursor-not-allowed
    `;

        const variants = {
            primary: `
        bg-amber-500 text-white
        hover:bg-amber-600
        focus:ring-amber-500
        shadow-sm hover:shadow-md
      `,
            secondary: `
        bg-white text-stone-700
        border border-stone-200
        hover:bg-stone-50 hover:border-stone-300
        focus:ring-amber-500
      `,
            ghost: `
        bg-transparent text-stone-600
        hover:bg-stone-100 hover:text-stone-900
        focus:ring-amber-500
      `,
            danger: `
        bg-red-500 text-white
        hover:bg-red-600
        focus:ring-red-500
      `,
        };

        const sizes = {
            sm: 'px-3 py-1.5 text-sm gap-1.5',
            md: 'px-4 py-2 text-sm gap-2',
            lg: 'px-6 py-3 text-base gap-2.5',
        };

        return (
            <motion.button
                ref={ref}
                type={type}
                whileHover={{ scale: disabled || isLoading ? 1 : 1.02 }}
                whileTap={{ scale: disabled || isLoading ? 1 : 0.98 }}
                className={cn(baseStyles, variants[variant], sizes[size], className)}
                disabled={disabled || isLoading}
                onClick={onClick}
            >
                {isLoading ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                ) : leftIcon ? (
                    <span className="flex-shrink-0">{leftIcon}</span>
                ) : null}

                {children}

                {rightIcon && !isLoading && (
                    <span className="flex-shrink-0">{rightIcon}</span>
                )}
            </motion.button>
        );
    }
);

Button.displayName = 'Button';

export default Button;
