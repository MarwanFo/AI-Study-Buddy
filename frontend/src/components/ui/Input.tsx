import { forwardRef } from 'react';
import type { InputHTMLAttributes, TextareaHTMLAttributes } from 'react';
import { cn } from '../../lib/utils';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
    error?: string;
    label?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
    ({ className, error, label, id, ...props }, ref) => {
        return (
            <div className="w-full">
                {label && (
                    <label
                        htmlFor={id}
                        className="block text-sm font-medium text-stone-600 mb-1.5"
                    >
                        {label}
                    </label>
                )}
                <input
                    ref={ref}
                    id={id}
                    className={cn(
                        `w-full px-4 py-2.5 rounded-xl
            bg-white border border-stone-200
            text-stone-900 placeholder:text-stone-400
            transition-all duration-200
            focus:outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-500
            disabled:opacity-50 disabled:cursor-not-allowed`,
                        error && 'border-red-500 focus:ring-red-500/50',
                        className
                    )}
                    {...props}
                />
                {error && (
                    <p className="mt-1.5 text-sm text-red-600">{error}</p>
                )}
            </div>
        );
    }
);

Input.displayName = 'Input';

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
    error?: string;
    label?: string;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
    ({ className, error, label, id, ...props }, ref) => {
        return (
            <div className="w-full">
                {label && (
                    <label
                        htmlFor={id}
                        className="block text-sm font-medium text-stone-600 mb-1.5"
                    >
                        {label}
                    </label>
                )}
                <textarea
                    ref={ref}
                    id={id}
                    className={cn(
                        `w-full px-4 py-3 rounded-xl
            bg-white border border-stone-200
            text-stone-900 placeholder:text-stone-400
            transition-all duration-200
            focus:outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-500
            disabled:opacity-50 disabled:cursor-not-allowed
            resize-none`,
                        error && 'border-red-500 focus:ring-red-500/50',
                        className
                    )}
                    {...props}
                />
                {error && (
                    <p className="mt-1.5 text-sm text-red-600">{error}</p>
                )}
            </div>
        );
    }
);

Textarea.displayName = 'Textarea';

export default Input;
