import { motion } from 'framer-motion'

export default function HeroSection() {
  return (
    <div className="w-full min-h-screen flex items-center justify-center py-32">
      <div className="container mx-auto px-8 max-w-8xl">
        <div className="flex flex-col lg:flex-row items-center justify-between gap-20">
          {/* Text Content */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="flex-1 text-center lg:text-left space-y-12"
          >
            <h1 className="text-7xl lg:text-8xl xl:text-9xl font-bold">
              <span className="block bg-clip-text text-transparent bg-gradient-to-r from-purple-200 to-pink-200">
                Julia Jakubowska
              </span>
            </h1>
            <div className="space-y-6">
              <motion.p 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="text-3xl lg:text-4xl text-purple-200 font-light"
              >
                AI-Powered Content Creation
              </motion.p>
              <motion.p 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="text-2xl lg:text-3xl text-purple-300 italic"
              >
                Kreacja Treści Wspierana Sztuczną Inteligencją
              </motion.p>
            </div>
            
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="space-y-4"
            >
              <p className="text-xl lg:text-2xl text-purple-200">
                Transform Your Ideas Into Engaging Content
              </p>
              <p className="text-xl lg:text-2xl text-purple-300 italic">
                Przekształć Swoje Pomysły w Angażujące Treści
              </p>
            </motion.div>
          </motion.div>

          {/* Profile Image */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative"
          >
            <div className="relative w-96 h-96 xl:w-[500px] xl:h-[500px]">
              <div className="absolute inset-0 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 animate-pulse blur-2xl opacity-50" />
              <img
                src="/julia-profile.jpg"
                alt="Julia Jakubowska"
                className="relative z-10 w-full h-full object-cover rounded-full border-8 border-purple-400/30"
              />
            </div>
            
            {/* Floating Elements */}
            <motion.div
              animate={{ 
                y: [0, -15, 0],
                rotate: [0, 5, 0]
              }}
              transition={{ 
                duration: 4,
                repeat: Infinity,
                ease: "easeInOut"
              }}
              className="absolute -top-12 -right-12 w-32 h-32 bg-purple-500/20 backdrop-blur-lg rounded-2xl flex items-center justify-center"
            >
              <span className="text-5xl">✨</span>
            </motion.div>
            
            <motion.div
              animate={{ 
                y: [0, 15, 0],
                rotate: [0, -5, 0]
              }}
              transition={{ 
                duration: 5,
                repeat: Infinity,
                ease: "easeInOut"
              }}
              className="absolute -bottom-8 -left-12 w-28 h-28 bg-pink-500/20 backdrop-blur-lg rounded-2xl flex items-center justify-center"
            >
              <span className="text-4xl">🎬</span>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}
