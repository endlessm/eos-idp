from django import template

register = template.Library()


@register.simple_tag
def social_account_display(social_account):
    """String to display for social account"""
    # Start with the string from the provider account
    provider_account = social_account.get_provider_account()
    display = str(provider_account)

    # Try to add the email address from the social account's extra data
    # using the provider's method for converting to standard field names
    provider = social_account.get_provider()
    common_fields = provider.extract_common_fields(social_account.extra_data)
    email = common_fields.get('email')
    if email:
        display += f' ({email})'

    return display
