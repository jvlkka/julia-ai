import { useState } from 'react'
import { motion } from 'framer-motion'

export default function Navigation() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-purple-900 to-purple-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <a href="/" className="text-2xl font-bold text-white">Julia AI</a>
          </motion.div>
          
          <motion.button
            onClick={() => setIsOpen(!isOpen)}
            className="sm:hidden inline-flex items-center justify-center p-2 rounded-md text-white hover:bg-purple-700 focus:outline-none"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
          >
            <span className="sr-only">Open main menu</span>
            {isOpen ? (
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </motion.button>
        </div>
      </div>

      {isOpen && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="sm:hidden"
        >
          <div className="px-2 pt-2 pb-3 space-y-1">
            <a
              href="/"
              className="block px-3 py-2 rounded-md text-white hover:bg-purple-700"
            >
              Dashboard
            </a>
          </div>
        </motion.div>
      )}
    </nav>
  )
}
