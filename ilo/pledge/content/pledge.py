from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
#from plone.multilingualbehavior.directives import languageindependent
from quintagroup.z3cform.captcha import Captcha, CaptchaWidgetFactory
from collective import dexteritytextindexer

from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.i18n.normalizer import idnormalizer

from zope.schema import ValidationError
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

from ilo.pledge import MessageFactory as _
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from plone.i18n.normalizer import idnormalizer
from ilo.pledge.content.pledge_detail import IPledgeDetail
# from ilo.socialsticker.content.sticker import ISticker
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.DCWorkflow.interfaces import IBeforeTransitionEvent, IAfterTransitionEvent
from z3c.form import validator
# Interface class; used to define content-type schema.


# countrieslist = SimpleVocabulary(
#     [SimpleTerm(value=u'Kabul', title=_(u'Kabul')),
#      SimpleTerm(value=u'Yerevan', title=_(u'Yerevan')),
#      SimpleTerm(value=u'Baku', title=_(u'Baku')),
#      SimpleTerm(value=u'Dhaka', title=_(u'Dhaka')),
#      SimpleTerm(value=u'Bahrain', title=_(u'Bahrain')),
#      SimpleTerm(value=u'Brunei', title=_(u'Brunei')),
#      SimpleTerm(value=u'Thimphu', title=_(u'Thimphu')),
#      SimpleTerm(value=u'Nicosia', title=_(u'Nicosia')),
#      SimpleTerm(value=u'Shanghai', title=_(u'Shanghai')),
#      SimpleTerm(value=u'Fiji', title=_(u'Fiji')),
#      SimpleTerm(value=u'Tbilisi', title=_(u'Tbilisi')),
#      SimpleTerm(value=u'Jakarta', title=_(u'Jakarta')),
#      SimpleTerm(value=u'Jerusalem', title=_(u'Jerusalem')),
#      SimpleTerm(value=u'Calcutta', title=_(u'Calcutta')),
#      SimpleTerm(value=u'Baghdad', title=_(u'Baghdad')),
#      SimpleTerm(value=u'Tehran', title=_(u'Tehran')),
#      SimpleTerm(value=u'Amman', title=_(u'Amman')),
#      SimpleTerm(value=u'Tokyo', title=_(u'Tokyo')),
#      SimpleTerm(value=u'Bishkek', title=_(u'Bishkek')),
#      SimpleTerm(value=u'Tarawa', title=_(u'Tarawa')),
#      SimpleTerm(value=u'Pyongyang', title=_(u'Pyongyang')),
#      SimpleTerm(value=u'Seoul', title=_(u'Seoul')),
#      SimpleTerm(value=u'Kuwait', title=_(u'Kuwait')),
#      SimpleTerm(value=u'Beirut', title=_(u'Beirut')),
#      SimpleTerm(value=u'Majuro', title=_(u'Majuro')),
#      SimpleTerm(value=u'Rangoon', title=_(u'Rangoon')),
#      SimpleTerm(value=u'Ulaanbaatar', title=_(u'Ulaanbaatar')),
#      SimpleTerm(value=u'Kuala Lumpur', title=_(u'Kuala Lumpur')),
#      SimpleTerm(value=u'Nauru', title=_(u'Nauru')),
#      SimpleTerm(value=u'Auckland', title=_(u'Auckland')),
#      SimpleTerm(value=u'Muscat', title=_(u'Muscat')),
#      SimpleTerm(value=u'Port Moresby', title=_(u'Port Moresby')),
#      SimpleTerm(value=u'Manila', title=_(u'Manila')),
#      SimpleTerm(value=u'Palau', title=_(u'Palau')),
#      SimpleTerm(value=u'Qatar', title=_(u'Qatar')),
#      SimpleTerm(value=u'Riyadh', title=_(u'Riyadh')),
#      SimpleTerm(value=u'Guadalcanal', title=_(u'Guadalcanal')),
#      SimpleTerm(value=u'Singapore', title=_(u'Singapore')),
#      SimpleTerm(value=u'Bangkok', title=_(u'Bangkok')),
#      SimpleTerm(value=u'Dushanbe', title=_(u'Dushanbe')),
#      SimpleTerm(value=u'Ashgabat', title=_(u'Ashgabat')),
#      SimpleTerm(value=u'Tongatapu', title=_(u'Tongatapu')),
#      SimpleTerm(value=u'Funafuti', title=_(u'Funafuti')),
#      SimpleTerm(value=u'Efate', title=_(u'Efate')),
#      SimpleTerm(value=u'Aden', title=_(u'Aden')),
#      SimpleTerm(value=u'Phnom Penh', title=_(u'Phnom Penh')),
#      SimpleTerm(value=u'Dili', title=_(u'Dili')),
#      SimpleTerm(value=u'Almaty', title=_(u'Almaty')),
#      SimpleTerm(value=u'Vientiane', title=_(u'Vientiane')),
#      SimpleTerm(value=u'Truk', title=_(u'Truk')),
#      SimpleTerm(value=u'Apia', title=_(u'Apia')),
#      SimpleTerm(value=u'Colombo', title=_(u'Colombo')),
#      SimpleTerm(value=u'Dubai', title=_(u'Dubai')),
#      SimpleTerm(value=u'Tahiti', title=_(u'Tahiti')),
#      SimpleTerm(value=u'Niue', title=_(u'Niue')),
#      SimpleTerm(value=u'Noumea', title=_(u'Noumea')),
#      SimpleTerm(value=u'Rarotonga', title=_(u'Rarotonga')),
#      SimpleTerm(value=u'Hong Kong', title=_(u'Hong Kong')),
#      SimpleTerm(value=u'Philippines', title=_(u'Philippines')),
#      SimpleTerm(value=u'Thailand', title=_(u'Thailand')),
#      SimpleTerm(value=u'Pago Pago', title=_(u'Pago Pago')),
#      SimpleTerm(value=u'Juba', title=_(u'Juba')),
#      SimpleTerm(value=u'North Korea', title=_(u'North Korea')),
#      SimpleTerm(value=u'South Korea', title=_(u'South Korea')),
#      SimpleTerm(value=u'Lebanon', title=_(u'Lebanon'))]
#     )

class InvalidEmailAddress(ValidationError):
    "Invalid email address"


# class stickers(object):
#     grok.implements(IContextSourceBinder)
#     def __call__(self,context ):
#         catalog = getToolByName(context, 'portal_catalog')
#         brains = catalog.unrestrictedSearchResults(object_provides = ISticker.__identifier__,sort_on='sortable_title', sort_order='ascending', review_state='published')
#         results = []
#         for brain in brains:
#             obj = brain._unrestrictedGetObject()
#             results.append(SimpleTerm(value=brain.UID, token=brain.UID, title=brain.getPath()))
#         return SimpleVocabulary(results)

#pledge detail vocabulary for dropdown

class countries(object):
    grok.implements(IContextSourceBinder)
    def __call__(self,context ):
        #countries = ['Kabul', 'Yerevan', 'Baku', 'Dhaka', 'Bahrain', 'Brunei', 'Thimphu', 'Nicosia', 'Shanghai', 'Fiji', 'Tbilisi', 'Jakarta', 'Jerusalem', 'Calcutta', 'Baghdad', 'Tehran', 'Amman', 'Tokyo', 'Bishkek', 'Tarawa', 'Pyongyang', 'Seoul', 'Kuwait', 'Beirut', 'Majuro', 'Rangoon', 'Ulaanbaatar', 'Kuala Lumpur','Nauru', 'Auckland','Muscat', 'Port Moresby', 'Manila', 'Palau', 'Qatar', 'Riyadh','Guadalcanal', 'Singapore', 'Bangkok', 'Dushanbe', 'Ashgabat','Tongatapu','Funafuti','Efate','Aden','Phnom Penh', 'Dili', 'Almaty', 'Vientiane', 'Truk', 'Apia', 'Colombo','Dubai', 'Tahiti', 'Niue', 'Noumea', 'Rarotonga', 'Hong Kong', 'Philippines', 'Thailand', 'Pago Pago', 'Juba', 'North Korea','South Korea', 'Lebanon','Peru','Mexico','Columbia']
        countries = ['Afghanistan','Akrotiri','Albania','Algeria','American Samoa','Andorra','Angola','Anguilla','Antarctica','Antigua and Barbuda','Argentina','Armenia','Aruba','Ashmore and Cartier Islands','Australia','Austria','Azerbaijan','Bahamas',' The','Bahrain','Bangladesh','Barbados','Bassas da India','Belarus','Belgium','Belize','Benin','Bermuda','Bhutan','Bolivia','Bosnia and Herzegovina','Botswana','Bouvet Island','Brazil','British Indian Ocean Territory','British Virgin Islands','Brunei','Bulgaria','Burkina Faso','Burma','Burundi','Cambodia','Cameroon','Canada','Cape Verde','Cayman Islands','Central African Republic','Chad','Chile','China','Christmas Island','Clipperton Island','Cocos (Keeling) Islands','Colombia','Comoros','Congo',' Democratic Republic of the','Congo',' Republic of the','Cook Islands','Coral Sea Islands','Costa Rica','Cote dIvoire','Croatia','Cuba','Cyprus','Czech Republic','Denmark','Dhekelia','Djibouti','Dominica','Dominican Republic','Ecuador','Egypt','El Salvador','Equatorial Guinea','Eritrea','Estonia','Ethiopia','Europa Island','Falkland Islands (Islas Malvinas)','Faroe Islands','Fiji','Finland','France','French Guiana','French Polynesia','French Southern and Antarctic Lands','Gabon','Gambia',' The','Gaza Strip','Georgia','Germany','Ghana','Gibraltar','Glorioso Islands','Greece','Greenland','Grenada','Guadeloupe','Guam','Guatemala','Guernsey','Guinea','Guinea-Bissau','Guyana','Haiti','Heard Island and McDonald Islands','Holy See (Vatican City)','Honduras','Hong Kong','Hungary','Iceland','India','Indonesia','Iran','Iraq','Ireland','Isle of Man','Israel','Italy','Jamaica','Jan Mayen','Japan','Jersey','Jordan','Juan de Nova Island','Kazakhstan','Kenya','Kiribati','Korea',' North','Korea',' South','Kuwait','Kyrgyzstan','Laos','Latvia','Lebanon','Lesotho','Liberia','Libya','Liechtenstein','Lithuania','Luxembourg','Macau','Macedonia','Madagascar','Malawi','Malaysia','Maldives','Mali','Malta','Marshall Islands','Martinique','Mauritania','Mauritius','Mayotte','Mexico','Micronesia',' Federated States of','Moldova','Monaco','Mongolia','Montserrat','Morocco','Mozambique','Namibia','Nauru','Navassa Island','Nepal','Netherlands','Netherlands Antilles','New Caledonia','New Zealand','Nicaragua','Niger','Nigeria','Niue','Norfolk Island','Northern Mariana Islands','Norway','Oman','Pakistan','Palau','Panama','Papua New Guinea','Paracel Islands','Paraguay','Peru','Philippines','Pitcairn Islands','Poland','Portugal','Puerto Rico','Qatar','Reunion','Romania','Russia','Rwanda','Saint Helena','Saint Kitts and Nevis','Saint Lucia','Saint Pierre and Miquelon','Saint Vincent and the Grenadines','Samoa','San Marino','Sao Tome and Principe','Saudi Arabia','Senegal','Serbia and Montenegro','Seychelles','Sierra Leone','Singapore','Slovakia','Slovenia','Solomon Islands','Somalia','South Africa','South Georgia and the South Sandwich Islands','Spain','Spratly Islands','Sri Lanka','Sudan','Suriname','Svalbard','Swaziland','Sweden','Switzerland','Syria','Taiwan','Tajikistan','Tanzania','Thailand','Timor-Leste','Togo','Tokelau','Tonga','Trinidad and Tobago','Tromelin Island','Tunisia','Turkey','Turkmenistan','Turks and Caicos Islands','Tuvalu','Uganda','Ukraine','United Arab Emirates','United Kingdom','United States','Uruguay','Uzbekistan','Vanuatu','Venezuela','Vietnam','Virgin Islands','Wake Island','Wallis and Futuna','West Bank','Western Sahara','Yemen','Zambia','Zimbabwe']
        results = []
        sorted_countries = countries.sort()
        for brain in countries:
            results.append(SimpleTerm(value=brain, token=brain, title=brain))
        return SimpleVocabulary(results)

class pledge_details(object):
    grok.implements(IContextSourceBinder)
    def __call__(self,context ):
        catalog = getToolByName(context, 'portal_catalog')
        #brains = catalog.unrestrictedSearchResults(object_provides = IPledgeDetail.__identifier__,sort_on='sortable_title', sort_order='ascending', review_state='published')
        if context.portal_type == 'ilo.pledge.pledgecampaign':
            path = '/'.join(context.getPhysicalPath())
        else:
            path = '/'.join(context.aq_parent.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.pledge.pledgedetail',review_state='published')
        results = []
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            results.append(SimpleTerm(value=brain.UID, token=brain.UID, title=obj.pledge_detail))
        return SimpleVocabulary(results)

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True

class IPledge(form.Schema, IImageScaleTraversable):
    """
    Pledge Form
    """
    form.widget(pledges=CheckBoxFieldWidget)
    pledges = schema.List(
        title=u'I commit to uphold the standards of Convention No. 189, and to protect and promote the rights of domestic workers in my home and community, by taking the following actions:',
        required=True,
        value_type=schema.Choice(source=pledge_details())
    )
    
    first_name = schema.TextLine(
           title=_(u"First Name"),
           required=True,
        )

    last_name = schema.TextLine(
           title=_(u"Last Name"),
           required=True,
        )


#    country = schema.TextLine(
#           title=_(u"Country"),
#           required=True,
#        )

    country = schema.Choice(title = u"Country", source=countries(), required=False)


#    domestic_workers = schema.Bool(
#        title=u'Employer of domestic worker/s',
#        required=False,
#        default=False
#    )

#this should be the id of the pledge
    email1 = schema.TextLine(
           title=_(u"Email Address"),
           constraint=validateaddress,
        )

    email2 = schema.TextLine(
           title=_(u"Verify Email Address"),
           constraint=validateaddress
        )

    
    # form.widget(stickers=CheckBoxFieldWidget)
    # stickers = schema.List(
    #     title=u'Stickers',
    #     required=True,
    #     value_type=schema.Choice(source=stickers())
    # )

    captcha = Captcha(
        title=_(u'Type the code'),
        description=_(u'Type the code from the picture shown below.'))
    
    @invariant
    def emailAddressValidation(self):
        #pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            
        if self.email1 != self.email2:
            raise Invalid(_("Both email addresses do not match"))
        
        #if not bool(re.match(pattern, self.email1)):
        #    raise Invalid(_(u"Email 1 is not a valid email address."))
        #elif not bool(re.match(pattern, self.email2  )):
        #    raise Invalid(_(u"Email 2 is not a valid email address."))


    pass

alsoProvides(IPledge, IFormFieldProvider)

class CheckDuplicateEmail(validator.SimpleFieldValidator):
    def validate(self, value):
        super(CheckDuplicateEmail, self).validate(value)
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        if context.portal_type == 'ilo.pledge.pledgecampaign':
            brains = catalog.unrestrictedSearchResults(object_provides = IPledge.__identifier__)
            emails = [brain._unrestrictedGetObject().email1 for brain in brains]
            if value in emails:
                raise Invalid(_("Email already exists."))
        elif context.portal_type == 'ilo.pledge.pledge':
            brains = catalog.unrestrictedSearchResults(object_provides = IPledge.__identifier__)
            emails = [brain._unrestrictedGetObject().email1 for brain in brains if brain.UID != self.context.UID()]
            if value in emails:
                raise Invalid(_("Email already exists."))
            

validator.WidgetValidatorDiscriminators(CheckDuplicateEmail, field=IPledge['email1'])
grok.global_adapter(CheckDuplicateEmail)


@grok.subscribe(IPledge, IObjectAddedEvent)
def _createObject(context, event):
    parent = context.aq_parent
    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    path = '/'.join(context.aq_parent.getPhysicalPath())
    brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1})
    for brain in brains:
        object_Ids.append(brain.id)
    
    email1 = str(idnormalizer.normalize(context.email1))
    new_id = email1.replace('-','_')
    
    test = ''
    num = 0
    if new_id in object_Ids:
        test = filter(lambda name: new_id in name, object_Ids)
        new_id = new_id +'_' + str(len(test))

    parent.manage_renameObject(id, new_id )
    context.setTitle(new_id)

    #exclude from navigation code
    behavior = IExcludeFromNavigation(context)
    behavior.exclude_from_nav = True

    context.reindexObject()
    return


@grok.subscribe(IPledge, IObjectModifiedEvent)
def modifyobject(context, event):
    parent = context.aq_parent
    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    path = '/'.join(context.aq_parent.getPhysicalPath())
    brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1})
    for brain in brains:
        object_Ids.append(brain.id)
    
    email1 = str(idnormalizer.normalize(context.email1))
    new_id = email1.replace('-','_')
    
    test = ''
    num = 0
    if new_id in object_Ids:
        test = filter(lambda name: new_id in name, object_Ids)
        new_id = new_id +'_' + str(len(test))

    parent.manage_renameObject(id, new_id )
    context.setTitle(new_id)

    #exclude from navigation code
    behavior = IExcludeFromNavigation(context)
    behavior.exclude_from_nav = True

    context.reindexObject()
    return

@grok.subscribe(IPledge, IAfterTransitionEvent)
def _changeState(context, event):
    wf = getToolByName(context, 'portal_workflow')
    curr_state = wf.getInfoFor(context, 'review_state')
    mailhost = getToolByName(context, 'MailHost')
    if curr_state == 'pending':
        context.plone_utils.addPortalMessage(_(u"Congratulations on taking the pledge."), "success")
        if context.email1:
            ## Email to afterfive
            mSubj = "Commitment Received"
            mFrom = "info@idwfed.org"
            mTo = "afterfive2015@gmail.com, info@idwfed.org"
            mBody = "A site visitor has just signed the c189 Pledge. Below are the details of the new commitment.\n"
            mBody += "Name: "+context.first_name+" "+context.last_name+"\n"
            #mBody += "City: "+context.city+"\n"
            mBody += "Country: "+context.country+"\n"
            mBody += "Email: "+context.email1+"\n"
            mBody += "\n"
            mBody += "To review the above commitment, visit:\n\n"
            mBody += context.absolute_url()+"\n\n"
            mBody += "To approve the post, click on the link below:\n\n"
            mBody += context.absolute_url()+"/content_status_modify?workflow_action=publish"
            mBody += "\n\n"
            
            mBody += "-------------------------\n"
            mBody += "IDWFED Portal"
            
            
            mSubj_1 = "Pledge Received"
            mTo_1 = context.email1
            mBody_1 = "This is to confirm that you have signed the c189 Pledge.  You may view your commitment details from the link below:\n\n"
            mBody_1 += context.absolute_url()+"\n\n"
            mBody_1 += "We will review your submission and once approved, your name will appear in the list of supporters.\n\n"
            mBody_1 += "If you find that there are errors to your submission, please email info@idwfed.org\n\n"
            mBody_1 += "If you would like us to keep you up-to-date with the latest information, please sign up for our newsletter at www.idwfed.org\n\n"
            mBody_1 += "\n\n\n"
            mBody_1 += "-------------------------\n"
            mBody_1 += "IDWFED Portal\n"
            mBody_1 += "http://www.idwfed.org"
            
            try:
                mailhost.send(mBody, mto=mTo, mfrom=mFrom, subject=mSubj, immediate=True, charset='utf8', msg_type=None)
                
                mailhost.send(mBody_1, mto=mTo_1, mfrom=mFrom, subject=mSubj_1, immediate=True, charset='utf8', msg_type=None)
            except ValueError, e:
                context.plone_utils.addPortalMessage(u'Unable to send email', 'info')
                return None


class PledgeAddForm(dexterity.AddForm):
    grok.name('ilo.pledge.pledge')
    template = ViewPageTemplateFile('templates/pledgeaddform.pt')
    form.wrap(False)
    

class PledgeEditForm(dexterity.EditForm):
    grok.context(IPledge)
    template = ViewPageTemplateFile('templates/pledgeeditform.pt')


