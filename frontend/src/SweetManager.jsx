import React, { useState, useEffect } from "react";
import {
    getSweets,
    createSweet,
    updateSweet,
    deleteSweet,
    restockSweet,
    purchaseSweet,
    searchSweets,
    isAdmin,
} from "./api";

const SweetManager = () => {
    const [sweets, setSweets] = useState([]);

    // Admin form state
    const [name, setName] = useState("");
    const [category, setCategory] = useState("");
    const [price, setPrice] = useState("");
    const [quantity, setQuantity] = useState("");
    const [editingId, setEditingId] = useState(null);

    // Search & filter state
    const [searchName, setSearchName] = useState("");
    const [searchCategory, setSearchCategory] = useState("");
    const [minPrice, setMinPrice] = useState("");
    const [maxPrice, setMaxPrice] = useState("");

    const [message, setMessage] = useState("");

    useEffect(() => {
        fetchSweets();
    }, []);

    const fetchSweets = async () => {
        try {
            const res = await getSweets();
            setSweets(res.data);
        } catch {
            setMessage("Error fetching sweets");
        }
    };

    const resetForm = () => {
        setName("");
        setCategory("");
        setPrice("");
        setQuantity("");
        setEditingId(null);
    };

    // ================= ADMIN CREATE / UPDATE =================

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage("");

        const payload = {
            name: name.trim(),
            category: category.trim(),
            price: Number(price),
            quantity: Number(quantity),
        };

        try {
            if (editingId) {
                await updateSweet(editingId, payload);
                setMessage("Sweet updated successfully");
            } else {
                await createSweet(payload);
                setMessage("Sweet added successfully");
            }

            resetForm();
            fetchSweets();
        } catch {
            setMessage("Operation failed. Check inputs.");
        }
    };

    // ================= SEARCH =================

    const handleSearch = async () => {
        const res = await searchSweets({
            name: searchName || undefined,
            category: searchCategory || undefined,
            min_price: minPrice || undefined,
            max_price: maxPrice || undefined,
        });

        setSweets(res.data);
    };

    return (
        <div className="sweet-manager-container">
            <h2>Sweet Inventory Management</h2>

            {/* ========== SEARCH & FILTERS (ALL USERS) ========== */}
            <div className="search-box">
                <h3>Search & Filter</h3>

                <input
                    placeholder="Search Name"
                    value={searchName}
                    onChange={(e) => setSearchName(e.target.value)}
                />

                <input
                    placeholder="Category"
                    value={searchCategory}
                    onChange={(e) => setSearchCategory(e.target.value)}
                />

                <input
                    type="number"
                    placeholder="Min Price"
                    value={minPrice}
                    onChange={(e) => setMinPrice(e.target.value)}
                />

                <input
                    type="number"
                    placeholder="Max Price"
                    value={maxPrice}
                    onChange={(e) => setMaxPrice(e.target.value)}
                />

                <button onClick={handleSearch}>Search</button>
                <button onClick={fetchSweets}>Reset</button>
            </div>

            {/* ========== ADMIN ONLY FORM ========== */}
            {isAdmin() && (
                <div className="create-sweet">
                    <h3>{editingId ? "Update Sweet" : "Add New Sweet"}</h3>

                    <form onSubmit={handleSubmit}>
                        <input
                            placeholder="Sweet Name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />

                        <input
                            placeholder="Category"
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                            required
                        />

                        <input
                            type="number"
                            placeholder="Price"
                            value={price}
                            onChange={(e) => setPrice(e.target.value)}
                            required
                        />

                        <input
                            type="number"
                            placeholder="Quantity"
                            value={quantity}
                            onChange={(e) => setQuantity(e.target.value)}
                            required
                        />

                        <button type="submit">
                            {editingId ? "Update Sweet" : "Add Sweet"}
                        </button>

                        {editingId && (
                            <button type="button" onClick={resetForm}>
                                Cancel
                            </button>
                        )}
                    </form>
                </div>
            )}

            <p className="message">{message}</p>

            {/* ========== INVENTORY LIST ========== */}
            <div className="sweet-list">
                <h3>Current Inventory</h3>

                {sweets.length === 0 ? (
                    <p>No sweets available</p>
                ) : (
                    <ul>
                        {sweets.map((sweet) => (
                            <li key={sweet.id}>
                                <strong>{sweet.name}</strong> ({sweet.category})
                                {" "}— ₹{sweet.price} | Qty: {sweet.quantity}

                                {/* ===== USER PURCHASE ===== */}
                                {!isAdmin() && (
                                    <button
                                        disabled={sweet.quantity === 0}
                                        onClick={async () => {
                                            await purchaseSweet(sweet.id);
                                            fetchSweets();
                                        }}
                                    >
                                        {sweet.quantity === 0 ? "Out of Stock" : "Purchase"}
                                    </button>
                                )}

                                {/* ===== ADMIN ACTIONS ===== */}
                                {isAdmin() && (
                                    <>
                                        <button
                                            onClick={() => {
                                                setEditingId(sweet.id);
                                                setName(sweet.name);
                                                setCategory(sweet.category);
                                                setPrice(sweet.price);
                                                setQuantity(sweet.quantity);
                                            }}
                                        >
                                            Edit
                                        </button>

                                        <button
                                            onClick={async () => {
                                                await deleteSweet(sweet.id);
                                                fetchSweets();
                                            }}
                                        >
                                            Delete
                                        </button>

                                        <button
                                            onClick={async () => {
                                                await restockSweet(sweet.id, 10);
                                                fetchSweets();
                                            }}
                                        >
                                            Restock +10
                                        </button>
                                    </>
                                )}
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
};

export default SweetManager;
