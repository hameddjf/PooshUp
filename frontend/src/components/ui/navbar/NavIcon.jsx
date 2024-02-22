/* eslint-disable react/prop-types */
function NavIcon({ icon, action }) {
  return (
    <li
      onClick={action}
      className="cursor-pointer list-none rounded-full p-4 transition-all duration-300 hover:bg-slate-200"
    >
      <img src={icon} alt="navigation icons"></img>
    </li>
  );
}

export default NavIcon;
