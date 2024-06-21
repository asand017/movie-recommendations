const Footer = ({className = ""} : {className?: string}) => {
    return (
        <footer className={`bg-gray-800 text-white ${className} w-screen`}>
          <div className="container mx-auto p-4">
            <p className="text-center">Footer</p>
          </div>
        </footer>
    )
}

export default Footer;