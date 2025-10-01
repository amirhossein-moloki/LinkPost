import Link from 'next/link';

const Sidebar = () => {
  const navItems = [
    { name: 'Content', href: '/content' },
    { name: 'Learning', href: '/learning' },
    { name: 'GitHub', href: '/github' },
    { name: 'Search', href: '/search' },
  ];

  return (
    <aside className="w-64 h-screen bg-gray-800 text-white p-4">
      <h2 className="text-2xl font-bold mb-6">Admin Panel</h2>
      <nav>
        <ul>
          {navItems.map((item) => (
            <li key={item.name} className="mb-2">
              <Link href={item.href} className="block p-2 rounded hover:bg-gray-700">
                {item.name}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;