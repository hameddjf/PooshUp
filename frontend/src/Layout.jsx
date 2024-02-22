import { Outlet } from "react-router-dom";
import Navbar from "./components/Navbar";

function Layout() {
  return (
    <>
      <Navbar />
      <main className="mt-[72px]">
        <Outlet />
      </main>
    </>
  );
}

export default Layout;
