/* eslint-disable no-unused-vars */
import home_icon from "../assets/icons/home-icon.svg";
import search_icon from "../assets/icons/search-icon.svg";
import menu_icon from "../assets/icons/menu-icon.svg";
import user_icon from "../assets/icons/user-icon.svg";
import cart_icon from "../assets/icons/cart-icon.svg";
import close_icon from "../assets/icons/close-icon.svg";
import { Link, NavLink } from "react-router-dom";
import NavIcon from "./ui/navbar/NavIcon";
import { useState } from "react";
import NavList from "./ui/navbar/NavIcon_desktop";

function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  return (
    <>
      {/* Mobile Nav */}
      <nav className="md:hidden">
        {/* Bottom */}
        <div className="fixed bottom-0 right-0 z-40 h-[64px] w-screen">
          <ul className="flex h-full items-center justify-between px-4 sm:p-8">
            <NavIcon
              action={() => setIsMenuOpen(!isMenuOpen)}
              icon={menu_icon}
            />
            <NavIcon icon={search_icon} />
            <NavLink className="[&.active>li]:bg-gray-300" to="/">
              <NavIcon icon={home_icon} />
            </NavLink>
            <NavLink className="[&.active>li]:bg-gray-300" to="/cart">
              <NavIcon icon={cart_icon} />
            </NavLink>
            <NavLink className="[&.active>li]:bg-gray-300" to="/profile">
              <NavIcon icon={user_icon} />
            </NavLink>
          </ul>
        </div>
        {/* animate-[slideIn_0.4s_ease-in-out] */}
        {/* Menu */}
        <div
          className={`${isMenuOpen ? "translate-x-full" : "-translate-x-full"} w-screenbg-white/50 fixed
           right-full top-0 z-40 h-screen backdrop-blur-md transition-all duration-500`}
        >
          <div className="p-4">
            <div className="flex w-full items-center justify-between">
              <button className="" onClick={() => setIsMenuOpen(false)}>
                <img src={close_icon} className="w-8" alt="close button" />
              </button>
              <h1>Logo</h1>
            </div>
            <hr className="my-6 border-slate-300" />
            <div className="">
              <ul className="flex w-full flex-col gap-4 text-lg font-[400] text-slate-700">
                <li>فروشگاه</li>
                <li>دسته بندی</li>
                <li>تماس با ما</li>
                <li>درباره ی ما</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Top */}
        <div className="fixed right-0 top-0 h-[72px] w-screen md:hidden">
          <ul className="flex h-full items-center justify-between px-4 shadow sm:p-8">
            <h1 className="">تماس با ما</h1>
            <h1>لوگو</h1>
          </ul>
        </div>
      </nav>

      {/* Desktop Nav */}
      <nav className="fixed right-0 top-0 hidden h-[80px] w-screen px-4 shadow md:block lg:px-12">
        <div className="pagecontainer mt-2">
          <div className=" flex h-[60px] items-center justify-between gap-8 lg:gap-16">
            <h1>Logo</h1>
            {/* <h1>Search</h1> */}
            <ul className="ml-auto flex h-full justify-between">
              <NavLink to="/" className="[&.active>li>span]:w-full">
                <NavList title="خانه" />
              </NavLink>
              <NavLink to="/shop" className="[&.active>li>span]:w-full">
                <NavList title="فروشگاه" />
              </NavLink>
              <NavLink to="/about" className="[&.active>li>span]:w-full">
                <NavList title="درباره ی ما" />
              </NavLink>
              <NavLink to="/contact" className="[&.active>li>span]:w-full">
                <NavList title="تماس با ما" />
              </NavLink>
              <NavList title="محصولات" />
            </ul>
            <div className="flex">
              <Link className="" to="/cart">
                <NavIcon icon={cart_icon} />
              </Link>
              <NavIcon icon={search_icon} />
              <Link className="" to="/profile">
                <NavIcon icon={user_icon} />
              </Link>
            </div>
          </div>
        </div>
      </nav>
    </>
  );
}

export default Navbar;
