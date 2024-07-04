const Header = ({className = ""} : {className?: string}) => {
    return (
        <header className={`bg-gray-800 text-white ${className} w-screen`}>
            <div className="container mx-auto p-2">
                <p className="text-center">Header</p>
            </div>
        </header>
    )
}

export default Header;