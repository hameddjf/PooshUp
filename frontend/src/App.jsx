/* eslint-disable no-unused-vars */
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import Home from "./pages/Home";
import Shop from "./pages/Shop";
import Blog from "./pages/Blog";
import Checkout from "./pages/Checkout";
import Product from "./pages/Product";
import Cart from "./pages/Cart";
import Signin from "./pages/Sign-in";
import Profile from "./pages/Profile";
import Layout from "./Layout";

const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      { path: "/", element: <Home /> },
      { path: "shop", element: <Shop /> },
      { path: "blog", element: <Blog /> },
      { path: "checkout", element: <Checkout /> },
      { path: "product/:id", element: <Product /> },
      { path: "cart", element: <Cart /> },
      { path: "profile", element: <Profile /> },
      { path: "about", element: <Home /> },
      { path: "contact", element: <Home /> },
    ],
  },
  { path: "sign-in", element: <Signin /> },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
