from zope.interface import classProvides
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.blueprint.base.blueprint import Source
from Products.CMFCore.utils import getToolByName


class ExportGroups(Source):
    classProvides(ISectionBlueprint)

    def getItems(self):
        pg = getToolByName(self.context, 'portal_groups')
        for group in pg.listGroups():
            tmp_item = group.__dict__
            tmp_item.update(group.getProperties())

            # see http://github.com/garbas/collective.blueprint.usersandgroups/
            def item_key(key):
                return '_group_%s' % key

            item = {}
            for k, v in tmp_item.items():
                item[item_key(k)] = v
            del(tmp_item)

            #setting roles
            item['_group_roles'] = group.getRoles()
            yield item


class ExportUsers(Source):
    """ see:
       http://blog.kagesenshi.org/2008/05/exporting-plone30-memberdata-and.html
    """
    classProvides(ISectionBlueprint)

    def getItems(self):
        item = {}
        memberdata_tool = getToolByName(self.context, 'portal_memberdata')

        properties = ['username', '_password'] + memberdata_tool.propertyIds()
        membership=getToolByName(self.context, 'portal_membership')
        passwdlist=self.context.acl_users.source_users._user_passwords

        # see http://github.com/garbas/collective.blueprint.usersandgroups/
        def item_key(key):
            return '_user_%s' % key

        for memberId in membership.listMemberIds():
            item = {}
            member = membership.getMemberById(memberId)
            for property in properties:
                if property == 'username':
                    item[item_key('username')] = memberId
                elif property == '_password':
                    item[item_key('_password')] = passwdlist[memberId]
                else:
                    item[item_key(property)] = member.getProperty(property)
            #setting global roles
            item['roles'] = member.getRoles()
            #setting groups
            item['groups'] = member.getGroups()
            yield item
