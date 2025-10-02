import Link from 'next/link';

const Sidebar = () => {
  const navItems = [
    { name: 'Dashboard', href: '/' },
    {
      name: 'Content',
      subItems: [
        { name: 'Posts', href: '/content' },
        { name: 'Campaigns', href: '/content/campaigns' },
        { name: 'Platforms', href: '/content/platforms' },
        { name: 'Tags', href: '/content/tags' },
      ],
    },
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
              {item.subItems ? (
                <div>
                  <span className="block p-2 text-gray-400">{item.name}</span>
                  <ul className="pl-4">
                    {item.subItems.map((subItem) => (
                      <li key={subItem.name} className="mb-1">
                        <Link href={subItem.href} className="block p-2 rounded hover:bg-gray-700">
                          {subItem.name}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : (
                <Link href={item.href} className="block p-2 rounded hover:bg-gray-700">
                  {item.name}
                </Link>
              )}
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;