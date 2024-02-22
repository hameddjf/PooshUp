/* eslint-disable react/prop-types */
function Helmet({ title }) {
  document.title = "CShop - " + title;
}

export default Helmet;
