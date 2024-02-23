/* eslint-disable react/prop-types */

/* eslint-disable no-unused-vars */
function NavList({ title, action }) {
  return (
    <li
      onClick={action}
      className="relative flex h-full cursor-pointer list-none items-center justify-center
        px-4 text-slate-700 lg:px-8 [&>span]:hover:w-full"
    >
      <p>{title}</p>
      <span
        className="absolute bottom-[-12px] right-0 h-[2.5px] w-0 
        bg-black transition-all duration-500"
      ></span>
    </li>
  );
}

export default NavList;
