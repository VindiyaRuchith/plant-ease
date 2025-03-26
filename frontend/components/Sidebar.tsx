// components/ui/Sidebar.tsx
'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Menu, X, Home, Info, FileText, ScanLine } from 'lucide-react';

export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    document.body.style.overflow = isOpen ? 'hidden' : 'auto';
  }, [isOpen]);

  return (
    <>
      {/* Menu Icon */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-4 left-4 z-[9999] p-2 bg-gray-800 text-white rounded shadow-lg hover:bg-gray-700 transition-all"
      >
        {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
      </button>

      {/* Sidebar Panel */}
      <div
        className={`fixed top-0 left-0 h-full w-64 backdrop-blur-lg bg-white/80 dark:bg-black/70 shadow-2xl transform transition-transform duration-300 ease-in-out z-[9998] ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full">
          {/* Sidebar Header */}
          <div className="p-6 border-b border-gray-300 dark:border-gray-700">
            <h2 className="text-xl font-bold text-gray-800 dark:text-gray-100">🌿 PlantEase</h2>
          </div>

          {/* Navigation Links */}
          <nav className="flex-1 flex flex-col gap-4 p-6 text-gray-700 dark:text-gray-200">
            <SidebarLink href="/" label="Home" icon={<Home />} onClick={() => setIsOpen(false)} />
            <SidebarLink href="/about" label="About Us" icon={<Info />} onClick={() => setIsOpen(false)} />
            <SidebarLink href="/terms" label="Terms of Service" icon={<FileText />} onClick={() => setIsOpen(false)} />
            <SidebarLink href="/scan" label="Scan Plant" icon={<ScanLine />} onClick={() => setIsOpen(false)} />
          </nav>
        </div>
      </div>

      {/* Backdrop */}
      {isOpen && (
        <div
          onClick={() => setIsOpen(false)}
          className="fixed inset-0 bg-black bg-opacity-40 z-[9990] backdrop-blur-sm transition-opacity"
        />
      )}
    </>
  );
}

// Reusable link component
function SidebarLink({
  href,
  label,
  icon,
  onClick,
}: {
  href: string;
  label: string;
  icon: React.ReactNode;
  onClick: () => void;
}) {
  return (
    <Link
      href={href}
      onClick={onClick}
      className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-green-100 dark:hover:bg-green-900 transition-all"
    >
      {icon}
      <span className="text-md">{label}</span>
    </Link>
  );
}
