db = db.getSiblingDB('admin');

db.createUser({
  user: 'mongo',
  pwd: 'example',
  roles: [
    { role: 'userAdminAnyDatabase', db: 'admin' },
    { role: 'readWriteAnyDatabase', db: 'admin' },
  ],
});