export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
          <span className="text-xl font-bold">DigiLicense</span>
          <nav className="flex items-center gap-6">
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">
              Features
            </a>
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">
              Pricing
            </a>
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">
              Docs
            </a>
            <button className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700">
              Get Started
            </button>
          </nav>
        </div>
      </header>

      <main className="flex flex-1 flex-col items-center justify-center px-4 text-center">
        <h1 className="text-5xl font-bold tracking-tight">
          Digital License Management
        </h1>
        <p className="mt-4 max-w-xl text-lg text-gray-600">
          Manage, track, and distribute your software licenses from one place.
        </p>
        <div className="mt-8 flex gap-4">
          <button className="rounded-lg bg-blue-600 px-6 py-3 font-medium text-white hover:bg-blue-700">
            Get Started
          </button>
          <button className="rounded-lg border border-gray-300 px-6 py-3 font-medium text-gray-700 hover:bg-gray-100">
            Learn More
          </button>
        </div>
      </main>

      <footer className="border-t border-gray-200 bg-white">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
          <span className="text-sm text-gray-500">
            &copy; 2026 DigiLicense
          </span>
          <div className="flex gap-4">
            <a href="#" className="text-sm text-gray-500 hover:text-gray-700">
              Privacy
            </a>
            <a href="#" className="text-sm text-gray-500 hover:text-gray-700">
              Terms
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
