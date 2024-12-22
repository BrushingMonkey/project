// main.js

// Load existing trades
async function loadTrades() {
    try {
        const response = await fetch('/trades');
        if (!response.ok) {
            console.error('Failed to fetch trades:', await response.json());
            return;
        }

        const trades = await response.json();
        const tbody = document.getElementById('tradeHistory');
        tbody.innerHTML = ''; // Clear existing rows
        trades.forEach(trade => {
            const positionClass = trade.position_type === 'long' ? 'text-green-400' : 'text-red-400';
            const row = `<tr class="table-row border-b border-gray-700">
                <td class="px-2 py-2">${trade.symbol}</td>
                <td class="px-2 py-2 ${positionClass}">${trade.position_type.toUpperCase()}</td>
                <td class="px-2 py-2">${trade.entry_price.toFixed(2)}</td>
                <td class="px-2 py-2">${trade.stop_loss_price ? trade.stop_loss_price.toFixed(2) : '-'}</td>
                <td class="px-2 py-2">${trade.take_profit_price ? trade.take_profit_price.toFixed(2) : '-'}</td>
                <td class="px-2 py-2">${trade.position_size.toFixed(2)}</td>
                <td class="px-2 py-2">${trade.potential_profit ? trade.potential_profit.toFixed(2) : '-'}</td>
                <td class="px-2 py-2">${trade.potential_loss ? trade.potential_loss.toFixed(2) : '-'}</td>
                <td class="px-2 py-2">${trade.risk_reward_ratio ? trade.risk_reward_ratio.toFixed(2) : '-'}</td>
                <td class="px-2 py-2">
                    <button onclick="deleteTrade(${trade.id})" class="text-red-400 hover:text-red-300">Delete</button>
                </td>
            </tr>`;
            tbody.innerHTML += row;
        });
    } catch (err) {
        console.error('Error loading trades:', err);
    }
}


// Delete a trade
async function deleteTrade(id) {
    try {
        const response = await fetch(`/trade/${id}`, { method: 'DELETE' });
        if (response.ok) {
            alert('Trade deleted successfully.');
            loadTrades(); // Reload the table after deletion
        } else {
            const error = await response.json();
            alert(`Error: ${error.error || 'Failed to delete trade'}`);
        }
    } catch (err) {
        console.error('Error deleting trade:', err);
        alert('An error occurred while deleting the trade.');
    }
}

// Handle form submission
document.getElementById('tradeForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent page reload
    const formData = new FormData(e.target);

    // Debugging: Log form data to ensure all fields are correct
    console.log('Form Data:', Object.fromEntries(formData.entries()));

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json();
            alert(`Error: ${error.error || 'Failed to calculate position'}`);
            return;
        }

        const result = await response.json();
        alert(`Position calculated: ${result.position_size.toFixed(6)}`);
        loadTrades(); // Reload trades
        e.target.reset(); // Clear the form
    } catch (err) {
        console.error('Error calculating position:', err);
        alert('An error occurred while calculating the position.');
    }
});

// Load trades on page load
document.addEventListener('DOMContentLoaded', loadTrades);
