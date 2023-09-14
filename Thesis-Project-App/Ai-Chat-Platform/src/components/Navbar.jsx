const Navbar = () => {
  return (
    <div className="navbar bg-base-300 w-full">
      <div className="flex-1">
        <a href="/" className="btn btn-ghost normal-case text-xl">
          Instant ChatMaker
        </a>
      </div>
      <div className="flex-none">
        <ul className="menu menu-horizontal px-1">
        <li>
            <a href="/">AIML Converter</a>
          </li>
          <li>
            <a href="/chatbot">Chatbot</a>
          </li>
          <li>
            <a href="/university">University Chatbot</a>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Navbar;
