// Small UI micro-interactions for the web UI
document.addEventListener('DOMContentLoaded', function(){
  // button click pulse
  document.querySelectorAll('button.primary').forEach(btn=>{
    btn.addEventListener('click', (e)=>{
      btn.animate([
        { transform: 'scale(1)', boxShadow: '0 8px 30px rgba(124,92,255,0.12)' },
        { transform: 'scale(0.98)', boxShadow: '0 6px 20px rgba(124,92,255,0.08)' },
        { transform: 'scale(1)', boxShadow: '0 8px 30px rgba(124,92,255,0.12)' }
      ], { duration: 220, easing: 'ease-out' });
    });
  });

  // float label effect: add class on focus
  document.querySelectorAll('input[type=text], select').forEach(el=>{
    el.addEventListener('focus', ()=> el.classList.add('focused'));
    el.addEventListener('blur', ()=> el.classList.remove('focused'));
  });

  // entrance animation for container
  const c = document.querySelector('.container');
  if(c){
    c.style.opacity = 0;
    c.style.transform = 'translateY(12px)';
    setTimeout(()=>{
      c.style.transition = 'opacity .45s ease, transform .45s ease';
      c.style.opacity = 1;
      c.style.transform = 'translateY(0)';
    }, 80);
  }
});
