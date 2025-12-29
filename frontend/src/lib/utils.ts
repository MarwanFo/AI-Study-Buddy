import { clsx, type ClassValue } from 'clsx';

/**
 * Combines class names with clsx
 * Utility for conditional classnames
 */
export function cn(...inputs: ClassValue[]) {
    return clsx(inputs);
}

/**
 * Format a date to relative time (e.g., "2 min ago")
 */
export function formatRelativeTime(date: Date): string {
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffSec = Math.floor(diffMs / 1000);
    const diffMin = Math.floor(diffSec / 60);
    const diffHour = Math.floor(diffMin / 60);
    const diffDay = Math.floor(diffHour / 24);

    if (diffSec < 60) return 'just now';
    if (diffMin < 60) return `${diffMin}m ago`;
    if (diffHour < 24) return `${diffHour}h ago`;
    if (diffDay < 7) return `${diffDay}d ago`;

    return date.toLocaleDateString();
}

/**
 * Truncate text with ellipsis
 */
export function truncate(text: string, maxLength: number): string {
    if (text.length <= maxLength) return text;
    return text.slice(0, maxLength - 3) + '...';
}

/**
 * Get file extension from filename
 */
export function getFileExtension(filename: string): string {
    const parts = filename.split('.');
    return parts.length > 1 ? parts.pop()!.toLowerCase() : '';
}

/**
 * Get file type label
 */
export function getFileTypeLabel(filename: string): string {
    const ext = getFileExtension(filename);
    const labels: Record<string, string> = {
        pdf: 'PDF',
        docx: 'Word',
        txt: 'Text',
        md: 'Markdown',
    };
    return labels[ext] || ext.toUpperCase();
}

/**
 * Generate a unique ID
 */
export function generateId(): string {
    return Math.random().toString(36).substr(2, 9);
}

/**
 * Delay utility for animations
 */
export function delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
}
