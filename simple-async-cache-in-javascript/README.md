## Simple async cache in Javascript

Secret in this gist is cache promise to avoid operation is awaited


```javascript
/**
 * @param {number} id
 * @param {(number) => Promise<import('./lib').CacheValue>} fetcher
 * @typedef {Object} Product
 * @property {number} id
 * @returns {Promise<Product>|undefined}
 */
async function getProductWithCached(id, fetcher) {
  const cachedKey = id.toString();

  const cached = lib.cache.get(cachedKey);

  if (!cached) {
    const pPromise = fetcher(id).catch(() => Promise.resolve());
    lib.cache.set(cachedKey, pPromise);
    return pPromise;
  }

  if (cached.isValid) {
    return cached.value;
  }

  const pPromise = fetcher(id).catch(() => Promise.resolve(cached.value));
  lib.cache.set(cachedKey, pPromise);
  return pPromise;
}

module.exports = {
  getProductWithCached,
};
```
