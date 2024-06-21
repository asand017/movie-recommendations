'use client';

import React, { useState } from 'react';

const PreferencesForm = () => {
    const [formData, setFormData] = useState({
        genres: [],
        runtime_range: 0,
        favorite_movies: [] // movie ids
    })

    const handleSubmit = (e: React.FormEvent) => {
        console.log("handleSubmit");
    }

    return(
        <form onSubmit={handleSubmit}>

        </form>
    )
}

export default PreferencesForm;