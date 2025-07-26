// src/pages/LandingPage.tsx

import { motion, useScroll, useTransform } from 'framer-motion';
import { Camera, BrainCircuit, Wallet, ArrowDown } from 'lucide-react';
import React from 'react';

// Reusable component for feature cards for cleaner code
const FeatureCard = ({ icon, title, description, index }: {
  icon: React.ReactNode;
  title: string;
  description: string;
  index: number;
}) => (
  <motion.div
    className="flex flex-col items-center p-6 text-center bg-white/5 rounded-2xl shadow-lg backdrop-blur-sm border border-white/10"
    initial={{ opacity: 0, y: 50 }}
    whileInView={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5, delay: index * 0.2 }}
    viewport={{ once: true }}
  >
    <div className="flex items-center justify-center w-16 h-16 mb-4 text-white bg-gradient-to-r from-blue-500 to-green-500 rounded-full">
      {icon}
    </div>
    <h3 className="mb-2 text-xl font-bold text-white">{title}</h3>
    <p className="text-gray-400">{description}</p>
  </motion.div>
);

// Reusable component for the "How it Works" steps
const HowItWorksStep = ({ num, title, description, index }: {
  num: string;
  title: string;
  description: string;
  index: number;
}) => (
    <motion.div
        className="flex items-start"
        initial={{ opacity: 0, x: -50 }}
        whileInView={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5, delay: index * 0.2 }}
        viewport={{ once: true }}
    >
        <div className="flex items-center justify-center w-12 h-12 mr-6 font-bold text-white bg-gradient-to-r from-red-500 to-yellow-400 rounded-full shrink-0">
            {num}
        </div>
        <div>
            <h3 className="text-xl font-bold text-white">{title}</h3>
            <p className="text-gray-400">{description}</p>
        </div>
    </motion.div>
);


export function LandingPage() {
    const { scrollYProgress } = useScroll();
    const scale = useTransform(scrollYProgress, [0, 0.3], [1, 0.95]);
    const opacity = useTransform(scrollYProgress, [0, 0.3], [1, 0]);

  // Variants for staggering animations in the hero section
  const heroContainerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
      },
    },
  };

  const heroItemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
      },
    },
  };

  return (
    <div className="min-h-screen font-sans text-white bg-gray-900">
      {/* --- Navigation/Header --- */}
      <motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="fixed top-0 left-0 right-0 z-50 px-6 py-4 bg-gray-900/80 backdrop-blur-md border-b border-white/10"
      >
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="text-2xl font-bold text-white">
            Project <span className="text-blue-500">R</span><span className="text-red-500">a</span><span className="text-yellow-500">s</span><span className="text-blue-500">e</span><span className="text-green-500">e</span><span className="text-red-500">d</span>
          </div>
          <nav className="hidden md:flex space-x-8">
            <a href="#features" className="text-gray-300 hover:text-white transition-colors">Features</a>
            <a href="#how-it-works" className="text-gray-300 hover:text-white transition-colors">How it Works</a>
          </nav>
        </div>
      </motion.header>

      {/* --- Hero Section --- */}
      <motion.section
        style={{ scale, opacity }}
        className="sticky top-0 flex flex-col items-center justify-center h-screen px-4 text-center bg-grid-white/[0.05]"
      >
        <motion.div
          variants={heroContainerVariants}
          initial="hidden"
          animate="visible"
          className="flex flex-col items-center"
        >
          <motion.div variants={heroItemVariants} className="mb-6">
            <h1 className="text-6xl font-extrabold tracking-tight md:text-7xl lg:text-8xl mb-2">
              <span className="text-blue-500">P</span><span className="text-red-500">r</span><span className="text-yellow-400">o</span><span className="text-blue-500">j</span><span className="text-green-500">e</span><span className="text-red-500">c</span><span className="text-yellow-400">t</span> <span className="text-blue-500">R</span><span className="text-red-500">a</span><span className="text-yellow-400">s</span><span className="text-blue-500">e</span><span className="text-green-500">e</span><span className="text-red-500">d</span>
            </h1>
            <div className="h-1 w-24 bg-gradient-to-r from-blue-500 via-red-500 via-yellow-400 via-green-500 to-red-500 mx-auto rounded-full"></div>
          </motion.div>
          <motion.h2 variants={heroItemVariants} className="text-4xl font-bold tracking-tight md:text-5xl lg:text-6xl mb-6">
            Your Receipts, Reimagined.
          </motion.h2>
          <motion.p variants={heroItemVariants} className="max-w-2xl mx-auto text-lg text-gray-300 md:text-xl">
            Snap a photo, get AI-powered insights, and save directly to your digital wallet. Managing expenses has never been this seamless.
          </motion.p>
          <motion.div variants={heroItemVariants} className="mt-8">
            <a
              href="/app" // This would link to your React App
              className="inline-block px-8 py-4 font-semibold text-white transition-all duration-300 bg-gradient-to-r from-blue-500 to-green-500 rounded-full shadow-lg hover:from-blue-600 hover:to-green-600 hover:scale-105 active:scale-95"
            >
              Launch Demo
            </a>
          </motion.div>
        </motion.div>
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 1, repeat: Infinity, repeatType: "reverse" }}
            className="absolute bottom-10"
        >
            <ArrowDown className="w-6 h-6 text-gray-400" />
        </motion.div>
      </motion.section>

    <div className="relative z-10 bg-gray-900">
      {/* --- Features Section --- */}
      <section id="features" className="py-20 md:py-32 px-4">
        <div className="max-w-5xl mx-auto">
          <motion.h2 
            className="mb-16 text-4xl font-bold text-center md:text-5xl"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            viewport={{ once: true }}
          >
            A Smarter Way to Track Finances
          </motion.h2>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            <FeatureCard 
              index={0}
              icon={<Camera size={32} />} 
              title="Effortless Scanning"
              description="Instantly capture every detail from your receipts with our advanced OCR technology."
            />
            <FeatureCard 
              index={1}
              icon={<BrainCircuit size={32} />} 
              title="Intelligent Insights"
              description="Our AI analyzes your spending patterns, categorizes expenses, and provides useful financial insights."
            />
            <FeatureCard 
              index={2}
              icon={<Wallet size={32} />} 
              title="Seamless Wallet Integration"
              description="Save warranties, tickets, and important receipts directly to your Google or Apple Wallet with one tap."
            />
          </div>
        </div>
      </section>

      {/* --- How It Works Section --- */}
      <section id="how-it-works" className="py-20 md:py-32 px-4 bg-black/20">
        <div className="max-w-3xl mx-auto">
          <motion.h2 
            className="mb-16 text-4xl font-bold text-center md:text-5xl"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            viewport={{ once: true }}
          >
            Three Simple Steps
          </motion.h2>
          <div className="flex flex-col gap-12">
             <HowItWorksStep 
                index={0}
                num="1" 
                title="Scan Your Receipt" 
                description="Use your phone's camera to snap a picture of any receipt or upload an existing image."
            />
             <HowItWorksStep 
                index={1}
                num="2" 
                title="AI Does The Work" 
                description="Our system instantly extracts the merchant, date, items, and total amount."
            />
             <HowItWorksStep 
                index={2}
                num="3" 
                title="Save & Analyze" 
                description="Save a digital copy to your wallet and view your spending data in the app dashboard."
            />
          </div>
        </div>
      </section>

      {/* --- Footer --- */}
      <footer className="py-8 text-center text-gray-500">
        <p>© {new Date().getFullYear()} Project Raseed. All rights reserved.</p>
      </footer>
    </div>
    </div>
  );
}