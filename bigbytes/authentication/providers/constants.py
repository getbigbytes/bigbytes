from bigbytes.authentication.oauth.constants import ProviderName
from bigbytes.authentication.providers.active_directory import ADProvider
from bigbytes.authentication.providers.azure_devops import AzureDevopsProvider
from bigbytes.authentication.providers.bitbucket import BitbucketProvider
from bigbytes.authentication.providers.ghe import GHEProvider
from bigbytes.authentication.providers.gitlab import GitlabProvider
from bigbytes.authentication.providers.google import GoogleProvider
from bigbytes.authentication.providers.oidc import OidcProvider
from bigbytes.authentication.providers.okta import OktaProvider

NAME_TO_PROVIDER = {
    ProviderName.ACTIVE_DIRECTORY: ADProvider,
    ProviderName.AZURE_DEVOPS: AzureDevopsProvider,
    ProviderName.BITBUCKET: BitbucketProvider,
    ProviderName.GHE: GHEProvider,
    ProviderName.GITLAB: GitlabProvider,
    ProviderName.GOOGLE: GoogleProvider,
    ProviderName.OIDC_GENERIC: OidcProvider,
    ProviderName.OKTA: OktaProvider,
}
