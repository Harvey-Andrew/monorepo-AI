export default defineNuxtRouteMiddleware((to) => {
  if (to.path === "/apps" || to.path === "/apps/") {
    return navigateTo("/");
  }
});
