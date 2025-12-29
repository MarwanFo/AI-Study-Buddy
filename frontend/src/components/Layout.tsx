import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BookOpen, Menu, X, AlertCircle, CheckCircle } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { cn } from '../lib/utils';
import DocumentUpload from './documents/DocumentUpload';
import DocumentList from './documents/DocumentList';
import ChatContainer from './chat/ChatContainer';

export function Layout() {
    const {
        sidebarOpen,
        toggleSidebar,
        systemStatus,
        checkSystem,
        documents,
        messages,
    } = useApp();

    // Check system on mount
    useEffect(() => {
        checkSystem();
    }, [checkSystem]);

    return (
        <div className="h-screen flex flex-col bg-stone-50 overflow-hidden">
            {/* Header */}
            <header className="flex-shrink-0 h-16 border-b border-stone-200 bg-white/80 backdrop-blur-sm">
                <div className="h-full px-4 lg:px-6 flex items-center justify-between">
                    {/* Left: Logo & Toggle */}
                    <div className="flex items-center gap-3">
                        <button
                            onClick={toggleSidebar}
                            className="lg:hidden p-2 rounded-xl hover:bg-stone-100 transition-colors"
                        >
                            {sidebarOpen ? (
                                <X className="w-5 h-5 text-stone-600" />
                            ) : (
                                <Menu className="w-5 h-5 text-stone-600" />
                            )}
                        </button>

                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center shadow-lg">
                                <BookOpen className="w-5 h-5 text-white" />
                            </div>
                            <div>
                                <h1 className="text-lg font-semibold text-stone-900">
                                    Study Buddy
                                </h1>
                                <p className="text-xs text-stone-500 hidden sm:block">
                                    AI-powered learning
                                </p>
                            </div>
                        </div>
                    </div>

                    {/* Right: Status & Actions */}
                    <div className="flex items-center gap-3">
                        {/* System status */}
                        <div className={cn(
                            'hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full text-sm',
                            systemStatus.modelsReady
                                ? 'bg-green-50 text-green-600'
                                : 'bg-red-50 text-red-600'
                        )}>
                            {systemStatus.modelsReady ? (
                                <>
                                    <CheckCircle className="w-4 h-4" />
                                    <span>Ready</span>
                                </>
                            ) : (
                                <>
                                    <AlertCircle className="w-4 h-4" />
                                    <span>Setup needed</span>
                                </>
                            )}
                        </div>

                        {/* Stats */}
                        {documents.length > 0 && (
                            <div className="hidden md:flex items-center gap-4 text-sm text-stone-500">
                                <span>{documents.length} docs</span>
                                <span>{messages.length} messages</span>
                            </div>
                        )}
                    </div>
                </div>
            </header>

            {/* Main content */}
            <div className="flex-1 flex overflow-hidden">
                {/* Sidebar */}
                <AnimatePresence mode="wait">
                    {sidebarOpen && (
                        <motion.aside
                            initial={{ width: 0, opacity: 0 }}
                            animate={{ width: 320, opacity: 1 }}
                            exit={{ width: 0, opacity: 0 }}
                            transition={{ duration: 0.3, ease: 'easeInOut' }}
                            className="flex-shrink-0 border-r border-stone-200 bg-white overflow-hidden"
                        >
                            <div className="w-80 h-full flex flex-col">
                                {/* Upload zone */}
                                <DocumentUpload />

                                {/* Divider */}
                                <div className="h-px bg-stone-100 mx-4" />

                                {/* Document list */}
                                <div className="flex-1 overflow-y-auto">
                                    <DocumentList />
                                </div>

                                {/* Footer */}
                                <div className="p-4 border-t border-stone-100">
                                    <div className="flex items-center justify-between text-xs text-stone-500">
                                        <span>100% free • Local AI</span>
                                        <span className="text-amber-600 font-medium">Ollama</span>
                                    </div>
                                </div>
                            </div>
                        </motion.aside>
                    )}
                </AnimatePresence>

                {/* Chat area */}
                <main className="flex-1 flex flex-col overflow-hidden bg-stone-50">
                    <ChatContainer />
                </main>
            </div>

            {/* System status alert (if not ready) */}
            {!systemStatus.modelsReady && (
                <motion.div
                    initial={{ y: 100 }}
                    animate={{ y: 0 }}
                    className="fixed bottom-4 left-1/2 -translate-x-1/2 bg-stone-900 text-white px-6 py-3 rounded-xl shadow-lg flex items-center gap-3"
                >
                    <AlertCircle className="w-5 h-5 text-amber-400" />
                    <div>
                        <p className="text-sm font-medium">Ollama not running</p>
                        <p className="text-xs text-stone-400">Run: ollama serve</p>
                    </div>
                </motion.div>
            )}
        </div>
    );
}

export default Layout;
