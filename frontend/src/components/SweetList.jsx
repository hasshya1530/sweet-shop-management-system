import { isAdmin } from "../api";
import { deleteSweet, purchaseSweet } from "../api";

const SweetList = ({ sweets, refresh }) => {
    return (
        <div>
            {sweets.map((sweet) => (
                <div key={sweet.id} className="sweet-card">
                    <strong>{sweet.name}</strong> – ₹{sweet.price}
                    <span> | Qty: {sweet.quantity}</span>

                    {/* PURCHASE (ALL USERS) */}
                    <button
                        disabled={sweet.quantity === 0}
                        onClick={() => {
                            purchaseSweet(sweet.id).then(refresh);
                        }}
                    >
                        Purchase
                    </button>

                    {/* ADMIN ACTIONS */}
                    {isAdmin() && (
                        <>
                            <button
                                onClick={() => {
                                    deleteSweet(sweet.id).then(refresh);
                                }}
                            >
                                Delete
                            </button>

                            <button
                                onClick={() => {
                                    // simple restock
                                    fetch(
                                        `http://localhost:8000/api/v1/sweets/${sweet.id}/restock?amount=10`,
                                        {
                                            method: "POST",
                                            headers: {
                                                Authorization: `Bearer ${localStorage.getItem("token")}`,
                                            },
                                        }
                                    ).then(refresh);
                                }}
                            >
                                Restock
                            </button>
                        </>
                    )}
                </div>
            ))}
        </div>
    );
};

export default SweetList;
