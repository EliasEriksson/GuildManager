from manager import Manager
from make_database import make_database
import exceptions
import aiounittest
import os


class TestManager(aiounittest.AsyncTestCase):
    def setUp(self):
        self.user_1 = (10, "Elias.4873", "123-abc")
        self.user_2 = (20, "madman.1234", "456-qwe")
        self.user_22 = (20, "blah.4567", "789-asd")
        self.user_3 = (30, "blah.4567", "789-asd")
        self.user_4 = (40, "blah.4567", "789-asd")

        self.server_1 = (1, 123456, "saar.1234", "123-asd", "kjsfhskjfdh")
        self.server_2 = (2, 654030, "pica.5432", "894389", "dgjeirew")
        self.server_22 = (2, 504935, "garosh.5456", "543-qwg", "gdflgjdd")
        self.server_3 = (3, 3287832, "maolumi.0994", "983298", "lkdslksd")

        self.user_server_1 = (10, 1)
        self.user_server_2 = (20, 2)
        self.user_server_3 = (30, 3)
        self.user_server_4 = (40, 4)

    @staticmethod
    async def remove_database(db):
        if os.path.isfile(db):
            os.remove(db)
            print(f"Removed old database '{db}'")
        pass

    async def remake_database(self, db):
        await self.remove_database(db)
        await make_database(db)

    async def test_get_users(self):
        db = "test_get_users.db"
        await self.remake_database(db)
        async with Manager(db) as manager:
            users = await manager.get_users()
            self.assertEqual(len(users), 0)

            await manager.add_user(*self.user_1)
            users = await manager.get_users()
            self.assertEqual(len(users), 1)

            await manager.add_user(*self.user_2)
            users = await manager.get_users()
            self.assertEqual(len(users), 2)

            for user in users:
                self.assertEqual(len(user.keys()), len(Manager.user_keys))
                for key in user.keys():
                    self.assertIn(key, Manager.user_keys)

        await self.remove_database(db)

    async def test_get_servers(self):
        db = "test_get_servers.db"
        await self.remake_database(db)
        async with Manager(db) as manager:
            servers = await manager.get_servers()
            self.assertEqual(len(servers), 0)

            await manager.add_server(*self.server_1)
            servers = await manager.get_servers()
            self.assertEqual(len(servers), 1)

            await manager.add_server(*self.server_2)
            servers = await manager.get_servers()
            self.assertEqual(len(servers), 2)

            for server in servers:
                self.assertEqual(len(server.keys()), len(Manager.server_keys))
                for key in server.keys():
                    self.assertIn(key, Manager.server_keys)

        await self.remove_database(db)

    async def test_get_user_server(self):
        db = "test_get_user_server.db"
        await self.remake_database(db)
        async with Manager(db) as manager:
            users = await manager.get_users()
            servers = await manager.get_servers()
            user_servers = await manager.get_users_servers()
            self.assertEqual(len(users), 0)
            self.assertEqual(len(servers), 0)
            self.assertEqual(len(user_servers), 0)

            await manager.add_user(*self.user_1)
            await manager.add_server(*self.server_1)
            await manager.add_user(*self.user_2)
            await manager.add_server(*self.server_2)

            await manager.add_user_server(*self.user_server_1)
            user_servers = await manager.get_users_servers()
            self.assertEqual(len(user_servers), 1)

            await manager.add_user_server(*self.user_server_2)
            user_servers = await manager.get_users_servers()
            self.assertEqual(len(user_servers), 2)

            for user_server in user_servers:
                self.assertEqual(len(user_server.keys()), len(Manager.user_server_keys))
                for key in user_server.keys():
                    self.assertIn(key, Manager.user_server_keys)

        await self.remove_database(db)

    async def test_add_user(self):
        db = "test_add_user.db"
        await self.remake_database(db)
        async with Manager(db) as manager:
            users = await manager.get_users()
            self.assertEqual(len(users), 0)

            await manager.add_user(*self.user_1)
            users = await manager.get_users()
            self.assertEqual(dict(zip(Manager.user_keys, self.user_1)), users[0])
            self.assertEqual(len(users), 1)

            await manager.add_user(*self.user_2)
            users = await manager.get_users()
            self.assertEqual(dict(zip(Manager.user_keys, self.user_2)), users[1])
            self.assertEqual(len(users), 2)

            with self.assertRaises(exceptions.UserAlreadyExcists):
                await manager.add_user(*self.user_22)

        await self.remove_database(db)

    async def test_add_server(self):
        db = "test_add_server.db"
        await self.remake_database(db)
        async with Manager(db) as manager:
            servers = await manager.get_servers()
            self.assertEqual(len(servers), 0)

            await manager.add_server(*self.server_1)
            servers = await manager.get_servers()
            self.assertEqual(dict(zip(Manager.server_keys, self.server_1)), servers[0])
            self.assertEqual(len(servers), 1)

            await manager.add_server(*self.server_2)
            servers = await manager.get_servers()
            self.assertEqual(dict(zip(Manager.server_keys, self.server_2)), servers[1])
            self.assertEqual(len(servers), 2)

            with self.assertRaises(exceptions.ServerAlreadyExcists):
                await manager.add_server(*self.server_22)

        await self.remove_database(db)

    async def test_add_user_server(self):
        db = "test_add_user_server.db"
        await self.remake_database(db)
        async with Manager(db) as manager:
            servers = await manager.get_servers()
            self.assertEqual(len(servers), 0)

            users = await manager.get_users()
            self.assertEqual(len(users), 0)

            user_servers = await manager.get_users_servers()
            self.assertEqual(len(user_servers), 0)

            await manager.add_server(*self.server_1)
            await manager.add_server(*self.server_2)
            await manager.add_server(*self.server_3)
            await manager.add_user(*self.user_1)
            await manager.add_user(*self.user_2)
            await manager.add_user(*self.user_4)

            await manager.add_user_server(*self.user_server_1)
            user_servers = await manager.get_users_servers()
            self.assertIn(dict(zip(Manager.user_server_keys, self.user_server_1)), user_servers)
            self.assertEqual(len(user_servers), 1)

            await manager.add_user_server(*self.user_server_2)
            user_servers = await manager.get_users_servers()
            self.assertIn(dict(zip(Manager.user_server_keys, self.user_server_2)), user_servers)
            self.assertEqual(len(user_servers), 2)

            with self.assertRaises(exceptions.MissingUser):
                await manager.add_user_server(*self.user_server_3)

            with self.assertRaises(exceptions.MissingServer):
                await manager.add_user_server(*self.user_server_4)

            await self.remove_database(db)

    async def test_remove_user(self):
        db = "test_remove_user.db"
        await self.remake_database(db)
        async with Manager(db) as manager:
            servers = await manager.get_servers()
            users_servers = await manager.get_users_servers()
            self.assertEqual(len(servers), 0)
            self.assertEqual(len(users_servers), 0)

            await manager.add_server(*self.server_2)
            await manager.add_server(*self.server_3)

            users = await manager.get_users()
            self.assertEqual(len(users), 0)

            await manager.add_user(*self.user_1)
            await manager.add_user(*self.user_2)
            await manager.add_user(*self.user_3)

            await manager.add_user_server(*self.user_server_2)
            await manager.add_user_server(*self.user_server_3)

            users = await manager.get_users()
            self.assertIn(dict(zip(Manager.user_keys, self.user_1)), users)
            self.assertIn(dict(zip(Manager.user_keys, self.user_2)), users)
            self.assertIn(dict(zip(Manager.user_keys, self.user_3)), users)
            self.assertEqual(len(users), 3)

            await manager.remove_user(10)
            users = await manager.get_users()
            self.assertIn(dict(zip(Manager.user_keys, self.user_2)), users)
            self.assertIn(dict(zip(Manager.user_keys, self.user_3)), users)
            self.assertEqual(len(users), 2)

            await manager.remove_user(20)
            users = await manager.get_users()
            users_servers = await manager.get_users_servers()
            self.assertIn(dict(zip(Manager.user_keys, self.user_3)), users)
            self.assertIn(dict(zip(Manager.user_server_keys, self.user_server_3)), users_servers)
            self.assertEqual(len(users), 1)
            self.assertEqual(len(users_servers), 1)

            await manager.remove_user(30)
            users = await manager.get_users()
            users_servers = await manager.get_users_servers()
            self.assertEqual(len(users), 0)
            self.assertEqual(len(users_servers), 0)

            with self.assertRaises(exceptions.MissingUser):
                await manager.remove_user(40)

        await self.remove_database(db)

    async def test_remove_server(self):
        db = "test_remove_server.db"
        await self.remake_database(db)
        async with Manager(db) as manager:
            users = await manager.get_users()
            users_servers = await manager.get_users_servers()
            self.assertEqual(len(users), 0)
            self.assertEqual(len(users_servers), 0)

            await manager.add_user(*self.user_2)
            await manager.add_user(*self.user_3)

            servers = await manager.get_servers()
            self.assertEqual(len(servers), 0)

            await manager.add_server(*self.server_1)
            await manager.add_server(*self.server_2)
            await manager.add_server(*self.server_3)

            await manager.add_user_server(*self.user_server_2)
            await manager.add_user_server(*self.user_server_3)

            servers = await manager.get_servers()
            self.assertIn(dict(zip(Manager.server_keys, self.server_1)), servers)
            self.assertIn(dict(zip(Manager.server_keys, self.server_2)), servers)
            self.assertIn(dict(zip(Manager.server_keys, self.server_3)), servers)
            self.assertEqual(len(servers), 3)

            await manager.remove_server(1)
            servers = await manager.get_servers()
            self.assertIn(dict(zip(Manager.server_keys, self.server_2)), servers)
            self.assertIn(dict(zip(Manager.server_keys, self.server_3)), servers)
            self.assertEqual(len(servers), 2)

            await manager.remove_server(2)
            servers = await manager.get_servers()
            users_servers = await manager.get_users_servers()
            self.assertIn(dict(zip(Manager.server_keys, self.server_3)), servers)
            self.assertIn(dict(zip(Manager.user_server_keys, self.user_server_3)), users_servers)
            self.assertEqual(len(servers), 1)
            self.assertEqual(len(users_servers), 1)

            await manager.remove_server(3)
            servers = await manager.get_servers()
            users_servers = await manager.get_users_servers()
            self.assertEqual(len(servers), 0)
            self.assertEqual(len(users_servers), 0)

            with self.assertRaises(exceptions.MissingServer):
                await manager.remove_server(4)

        await self.remove_database(db)

    async def test_unlink_user(self):
        db = "test_unlink_user.db"
        await self.remake_database(db)
        async with Manager(db) as manager:
            servers = await manager.get_servers()
            users = await manager.get_users()
            users_servers = await manager.get_users_servers()
            self.assertEqual(len(servers), 0)
            self.assertEqual(len(users), 0)
            self.assertEqual(len(users_servers), 0)

            await manager.add_server(*self.server_1)
            await manager.add_server(*self.server_2)
            await manager.add_server(*self.server_3)
            await manager.add_user(*self.user_1)
            await manager.add_user(*self.user_2)
            await manager.add_user(*self.user_3)

            await manager.add_user_server(*self.user_server_1)
            await manager.add_user_server(*self.user_server_2)
            await manager.add_user_server(*self.user_server_3)

            users_servers = await manager.get_users_servers()
            self.assertIn(dict(zip(Manager.user_server_keys, self.user_server_1)), users_servers)
            self.assertIn(dict(zip(Manager.user_server_keys, self.user_server_2)), users_servers)
            self.assertIn(dict(zip(Manager.user_server_keys, self.user_server_3)), users_servers)
            self.assertEqual(len(users_servers), 3)

            await manager.unlink_user(10, 1)
            users_servers = await manager.get_users_servers()
            self.assertIn(dict(zip(Manager.user_server_keys, self.user_server_2)), users_servers)
            self.assertIn(dict(zip(Manager.user_server_keys, self.user_server_3)), users_servers)
            self.assertEqual(len(users_servers), 2)

            await manager.unlink_user(20, 2)
            users_servers = await manager.get_users_servers()
            self.assertIn(dict(zip(Manager.user_server_keys, self.user_server_3)), users_servers)
            self.assertEqual(len(users_servers), 1)

            await manager.unlink_user(30, 3)
            users_servers = await manager.get_users_servers()
            self.assertEqual(len(users_servers), 0)

            with self.assertRaises(exceptions.MissingUsersServer):
                await manager.unlink_user(40, 4)

        await self.remove_database(db)


if __name__ == '__main__':
    pass
