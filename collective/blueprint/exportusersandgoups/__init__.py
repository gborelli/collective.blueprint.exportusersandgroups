from zope.interface import classProvides
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.blueprint.base.blueprint import Source
from Products.CMFCore.utils import getToolByName

class ExportGroups(object):
    pass


# see http://blog.kagesenshi.org/2008/05/exporting-plone30-memberdata-and.html
class ExportUsers(Source):

    classProvides(ISectionBlueprint)

    def getItems(self):
        item = {}
        memberdata_tool = getToolByName(self.context, 'portal_memberdata')

        properties = ['username','_password'] + memberdata_tool.propertyIds()

        membership=getToolByName(self.context, 'portal_membership')
        passwdlist=self.context.acl_users.source_users._user_passwords

        # see http://github.com/garbas/collective.blueprint.usersandgroups/
        def item_key(key):
            return '_user_%s' % key

        for memberId in membership.listMemberIds():
            item = {}
            for property in properties:
                if property == 'member_id':
                   item[item_key('username')] = memberId
                elif property == 'password':
                   item[item_key('_password')] = passwdlist[memberId]
                else:
                   member = membership.getMemberById(memberId)
                   item[item_key(property)] = member.getProperty(property)
            yield item
