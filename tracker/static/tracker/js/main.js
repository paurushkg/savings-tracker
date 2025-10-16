document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const savingsBoxes = document.querySelectorAll('.savings-box');
    const progressFill = document.querySelector('.progress-fill');
    const progressPercentageElement = document.querySelector('.progress-percentage');
    const savedAmountElement = document.querySelector('.saved-amount');
    const regenerateBtn = document.getElementById('regenerate-btn');
    const loadingOverlay = document.getElementById('loading-overlay');

    // Initialize
    let currentSavedAmount = window.savedAmount || 0;
    let currentTotalAmount = window.totalAmount || 100000;
    let currentProgressPercentage = window.progressPercentage || 0;

    // Add click event listeners to all savings boxes
    savingsBoxes.forEach(box => {
        box.addEventListener('click', function() {
            toggleSavingsBox(this);
        });
    });

    // Add event listeners to control buttons
    regenerateBtn.addEventListener('click', regenerateBoxes);

    function toggleSavingsBox(boxElement) {
        const boxId = boxElement.dataset.boxId;
        const boxValue = parseInt(boxElement.dataset.value);
        const isSaved = boxElement.classList.contains('saved');
        
        // Prevent multiple clicks during animation
        if (boxElement.classList.contains('saving')) {
            return;
        }

        // If box is already saved and user wants to unsave it, ask for confirmation
        if (isSaved) {
            if (!confirm(`Are you sure you want to remove ₹${boxValue.toLocaleString()} from your savings?`)) {
                return; // User cancelled, don't proceed
            }
        }

        // Add saving animation class
        boxElement.classList.add('saving');

        // Send AJAX request to toggle box
        fetch(`/toggle/${boxId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update box visual state
                if (data.is_saved) {
                    boxElement.classList.add('saved');
                } else {
                    boxElement.classList.remove('saved');
                }

                // Update progress tracking
                updateProgress(data.saved_amount, data.total_amount, data.progress_percentage);
                
                // Add celebration effect for savings
                if (data.is_saved) {
                    addCelebrationEffect(boxElement);
                }
            } else {
                console.error('Error toggling box:', data.error);
                showNotification('Error updating savings box', 'error');
            }
        })
        .catch(error => {
            console.error('Network error:', error);
            showNotification('Network error occurred', 'error');
        })
        .finally(() => {
            // Remove saving animation class
            setTimeout(() => {
                boxElement.classList.remove('saving');
            }, 300);
        });
    }

    function updateProgress(savedAmount, totalAmount, progressPercentage) {
        // Update progress bar
        progressFill.style.width = `${progressPercentage}%`;
        
        // Update progress text
        progressPercentage = Math.round(progressPercentage * 10) / 10; // Round to 1 decimal
        progressPercentageElement.textContent = `${progressPercentage}% Complete`;
        
        // Update saved amount
        animateNumber(savedAmountElement, currentSavedAmount, savedAmount, '₹');
        
        // Update current values
        currentSavedAmount = savedAmount;
        currentTotalAmount = totalAmount;
        currentProgressPercentage = progressPercentage;

        // Check if goal reached
        if (progressPercentage >= 100) {
            showGoalReachedCelebration();
        }
    }

    function animateNumber(element, startValue, endValue, prefix = '') {
        const duration = 500;
        const startTime = performance.now();
        const difference = endValue - startValue;

        function animate(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function for smooth animation
            const easedProgress = 1 - Math.pow(1 - progress, 3);
            
            const currentValue = Math.round(startValue + (difference * easedProgress));
            element.textContent = `${prefix}${currentValue.toLocaleString()}`;

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        }

        requestAnimationFrame(animate);
    }

    function addCelebrationEffect(boxElement) {
        // Create sparkle effect
        for (let i = 0; i < 5; i++) {
            setTimeout(() => {
                createSparkle(boxElement);
            }, i * 100);
        }
    }

    function createSparkle(element) {
        const sparkle = document.createElement('div');
        sparkle.style.position = 'absolute';
        sparkle.style.width = '6px';
        sparkle.style.height = '6px';
        sparkle.style.background = '#FFD700';
        sparkle.style.borderRadius = '50%';
        sparkle.style.pointerEvents = 'none';
        sparkle.style.zIndex = '1000';
        
        const rect = element.getBoundingClientRect();
        const x = rect.left + Math.random() * rect.width;
        const y = rect.top + Math.random() * rect.height;
        
        sparkle.style.left = `${x}px`;
        sparkle.style.top = `${y}px`;
        
        document.body.appendChild(sparkle);
        
        // Animate sparkle
        const animation = sparkle.animate([
            { 
                transform: 'scale(0) rotate(0deg)',
                opacity: 1
            },
            { 
                transform: 'scale(1) rotate(180deg)',
                opacity: 1
            },
            { 
                transform: 'scale(0) rotate(360deg)',
                opacity: 0
            }
        ], {
            duration: 800,
            easing: 'cubic-bezier(0.4, 0.0, 0.2, 1)'
        });
        
        animation.onfinish = () => {
            sparkle.remove();
        };
    }

    function showGoalReachedCelebration() {
        // Create confetti effect
        for (let i = 0; i < 50; i++) {
            setTimeout(() => {
                createConfetti();
            }, i * 50);
        }
        
        // Show congratulations message
        showNotification('🎉 Congratulations! You\'ve reached your ₹1,00,000 savings goal!', 'success', 5000);
    }

    function createConfetti() {
        const confetti = document.createElement('div');
        confetti.style.position = 'fixed';
        confetti.style.width = '10px';
        confetti.style.height = '10px';
        confetti.style.background = `hsl(${Math.random() * 360}, 100%, 50%)`;
        confetti.style.borderRadius = '50%';
        confetti.style.pointerEvents = 'none';
        confetti.style.zIndex = '1001';
        confetti.style.left = `${Math.random() * window.innerWidth}px`;
        confetti.style.top = '-10px';
        
        document.body.appendChild(confetti);
        
        const animation = confetti.animate([
            {
                transform: 'translateY(0) rotate(0deg)',
                opacity: 1
            },
            {
                transform: `translateY(${window.innerHeight + 10}px) rotate(720deg)`,
                opacity: 0
            }
        ], {
            duration: Math.random() * 2000 + 1000,
            easing: 'cubic-bezier(0.4, 0.0, 0.2, 1)'
        });
        
        animation.onfinish = () => {
            confetti.remove();
        };
    }


    function regenerateBoxes() {
        if (confirm('Generate a new savings challenge? This will create new boxes with different values.')) {
            showLoading();
            
            fetch('/initialize/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    showNotification('Error generating new challenge', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Network error occurred', 'error');
            })
            .finally(() => {
                hideLoading();
            });
        }
    }

    function showLoading() {
        loadingOverlay.style.display = 'flex';
    }

    function hideLoading() {
        loadingOverlay.style.display = 'none';
    }

    function showNotification(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Styles for notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '15px 20px',
            borderRadius: '8px',
            color: 'white',
            fontWeight: '600',
            zIndex: '1002',
            maxWidth: '400px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease'
        });

        // Set background color based on type
        switch (type) {
            case 'success':
                notification.style.background = '#4CAF50';
                break;
            case 'error':
                notification.style.background = '#F44336';
                break;
            case 'warning':
                notification.style.background = '#FF9800';
                break;
            default:
                notification.style.background = '#2196F3';
        }

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Animate out and remove
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, duration);
    }

    function getCSRFToken() {
        // Try to get CSRF token from cookie
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        
        // If not found in cookie, try to get from meta tag
        if (!cookieValue) {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
            if (csrfToken) {
                cookieValue = csrfToken.value;
            }
        }
        
        return cookieValue || '';
    }

    // Add some entrance animations
    function addEntranceAnimations() {
        savingsBoxes.forEach((box, index) => {
            box.style.opacity = '0';
            box.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                box.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                box.style.opacity = '1';
                box.style.transform = 'translateY(0)';
            }, index * 30);
        });
    }

    // Initialize entrance animations
    addEntranceAnimations();
});