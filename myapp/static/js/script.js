document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('searchInput');
    const productCards = document.querySelectorAll('.product-card');
  
    input.addEventListener('input', function () {
      const query = input.value.toLowerCase();
  
      productCards.forEach(card => {
        const title = card.querySelector('.card-title').textContent.toLowerCase();
        if (title.includes(query)) {
          card.style.display = 'block';  // показать
        } else {
          card.style.display = 'none';   // скрыть
        }
      });
    });
  });
  window.addEventListener("load", () => {
    // Grouping elements for stagger animation
    const elementsToAnimate = [
      "#form-title",
      "#email-input",
      "#password-input",
      "#remember-me",
      "#forgot-password",
      "#sign-in-button",
    ];
  
    // Applying stagger with GSAP
    gsap.from(elementsToAnimate, {
      opacity: 0,
      y: -30,
      duration: 0.6,
      ease: "power2.out",
      stagger: 0.2,
    });
  
    // Input fields animation on focus
    document.querySelectorAll("input").forEach((input) => {
      input.addEventListener("focus", () => {
        gsap.to(input, {
          scale: 1.05,
          boxShadow: "0px 4px 20px rgba(0, 128, 128, 0.4)",
          duration: 0.3,
          ease: "power2.out",
        });
      });
      input.addEventListener("blur", () => {
        gsap.to(input, {
          scale: 1,
          boxShadow: "0px 0px 0px rgba(0, 0, 0, 0)",
          duration: 0.3,
          ease: "power2.in",
        });
      });
    });
  
    // Forgot Password link animation on click
    const forgotPasswordLink = document.querySelector("#forgot-password");
    forgotPasswordLink.addEventListener("click", (e) => {
      e.preventDefault();
      gsap.to(forgotPasswordLink, {
        color: "#ff6347",
        duration: 0.3,
        ease: "power2.out",
        yoyo: true,
        repeat: 1,
      });
    });
  
    // Button hover animation
    const signInButton = document.querySelector("button");
    signInButton.addEventListener("mouseenter", () => {
      gsap.to(signInButton, {
        scale: 1.1,
        boxShadow: "0px 4px 20px rgba(0, 128, 128, 0.4)",
        duration: 0.3,
        ease: "power2.out",
      });
    });
    signInButton.addEventListener("mouseleave", () => {
      gsap.to(signInButton, {
        scale: 1,
        boxShadow: "0px 0px 0px rgba(0, 0, 0, 0)",
        duration: 0.3,
        ease: "power2.in",
      });
    });
  });
