import { Outlet } from "react-router-dom";
import Navbar from "./components/Navbar";

function Layout() {
  return (
    <>
      <Navbar />
      <main className="mt-[72px] md:mt-[80px]">
        <Outlet />
      </main>
    </>
  );
}

export default Layout;
