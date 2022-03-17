// @ts-nocheck

import React from "react";
import { Box, Text, Flex, Image, Spacer } from "@chakra-ui/react";
import PageTitle from "../components/PageTitle";
import LeftCard, { assignCards } from "../components/InfoCard";
import torch from '../public/assets/Initiative_logos/conservatism_logo_2.png'
import individual from '../public/assets/Initiative_logos/libertarianism_logo.png'
import triangleCircle from '../public/assets/Initiative_logos/progressivism_logo_2.png'
import ladyJustice from '../public/assets/Initiative_logos/neutral_logo_2.png'
import crown from '../public/assets/Initiative_logos/radical_conservatism_logo.png'
import fist from '../public/assets/Initiative_logos/radical_progressivism_logo.png'
import pheonix from '../public/assets/Initiative_logos/radical_progressivism_logo_2.png'
import trident from '../public/assets/Initiative_logos/libertariansim_logo_2_.png'
import bible from '../public/assets/Initiative_logos/radical_conservatism_logo_3.png'
import pidgeon from '../public/assets/Initiative_logos/progressivism_logo.png'
import lion from '../public/assets/Initiative_logos/conservatism_logo.png'
import owl from '../public/assets/Initiative_logos/neutral_logo.png'
import { Banner } from "../components/TheHeader";
import axios from "axios";
import { useState } from "react";
import Popups from "../components/Popup";

const INITIATIVE_MAP = {
  1: "Conservatism",
  2: "Progressivism",
  3: "Libertarianism",
  4: "Activism",
  5: "Technocratism",
  6: "Socialism",
  7: "Statism",
  8: "Nationalism"
}

/**
 * NOTE: all initiative descriptions have been scraped from the first two paragraphs of their corresponding wikipedia articles
 */
const INITIATIVES = [
  {
    title: "Conservatism",
    content: `Conservatism is the aesthetic, cultural, social, and political outlook that embodies the desire to conserve existing things, held to be either good in themselves, or better than the likely alternatives, or at least safe, familiar, and the objects of trust and affection.

    The central tenets of conservatism may vary in relation to the traditions and values of the culture and civilization in which it appears. In Western culture, conservatives seek to conserve a range of things such as organized religion, property rights, parliamentary government, family values, the natural environment, and classical and vernacular architecture. Adherents of conservatism often oppose modernism and seek a return to traditional values.
    
    The first established use of the term in a political context originated in 1818 with François-René de Chateaubriand during the period of Bourbon Restoration that sought to roll back the policies of the French Revolution. Historically associated with right-wing politics, the term has since been used to describe a wide range of views. There is no single set of policies regarded as conservative because the meaning of conservatism depends on what is considered traditional in a given place and time. Conservative thought has varied considerably as it has adapted itself to existing traditions and national cultures. For example, some conservatives advocate for greater government intervention in the economy while others advocate for a more laissez faire free market economic system. Thus conservatives from different parts of the world—each upholding their respective traditions—may disagree on a wide range of issues. Edmund Burke, an 18th-century politician who opposed the French Revolution, but supported the American Revolution, is credited as one of the main theorists of conservatism in the 1790s.
    `,
    imageUrl: torch
  },
  {
    title: `Libertarianism`,
    content: `Libertarianism (from French: libertaire, "libertarian"; from Latin: libertas, "freedom") is a political philosophy and movement that upholds liberty as a core principle. Libertarians seek to maximize autonomy and political freedom, emphasizing free association, freedom of choice, individualism and voluntary association. Libertarians share a skepticism of authority and state power, but some libertarians diverge on the scope of their opposition to existing economic and political systems. Various schools of libertarian thought offer a range of views regarding the legitimate functions of state and private power, often calling for the restriction or dissolution of coercive social institutions. Different categorizations have been used to distinguish various forms of libertarianism. Scholars distinguish libertarian views on the nature of property and capital, usually along left–right or socialist–capitalist lines.

    Libertarianism originated as a form of left-wing politics such as anti-authoritarian and anti-state socialists like anarchists, especially social anarchists, but more generally libertarian communists/Marxists and libertarian socialists. These libertarians seek to abolish capitalism and private ownership of the means of production, or else to restrict their purview or effects to usufruct property norms, in favor of common or cooperative ownership and management, viewing private property as a barrier to freedom and liberty. Left-libertarian ideologies include anarchist schools of thought, alongside many other anti-paternalist and New Left schools of thought centered around economic egalitarianism as well as geolibertarianism, green politics, market-oriented left-libertarianism and the Steiner–Vallentyne school.
    
    In the mid-20th century, right-libertarian proponents of anarcho-capitalism and minarchism co-opted the term libertarian to advocate laissez-faire capitalism and strong private property rights such as in land, infrastructure and natural resources. The latter is the dominant form of libertarianism in the United States, where it advocates civil liberties, natural law, free-market capitalism and a major reversal of the modern welfare state. 
    `,
    imageUrl: individual,
  },
  {
    title: `Progressivism`,
    content: `Progressivism is a political philosophy in support of social reform. Based on the idea of progress in which advancements in science, technology, economic development and social organization are vital to the improvement of the human condition, progressivism became highly significant during the Age of Enlightenment in Europe, out of the belief that Europe was demonstrating that societies could progress in civility from uncivilized conditions to civilization through strengthening the basis of empirical knowledge as the foundation of society. Figures of the Enlightenment believed that progress had universal application to all societies and that these ideas would spread across the world from Europe.

    The contemporary common political conception of progressivism emerged from the vast social changes brought about by industrialization in the Western world in the late-19th century. Progressives take the view that progress is being stifled by vast economic inequality between the rich and the poor; minimally regulated laissez-faire capitalism with monopolistic corporations; and the intense and often violent conflict between those perceived to be privileged and unprivileged, arguing that measures were needed to address these problems.
    
    The meaning of progressivism has varied over time and differs depending on perspective. Early-20th century progressivism was tied to eugenics and the temperance movement, both of which were promoted in the name of public health and as initiatives toward that goal. Contemporary progressives promote public policies that they believe will lead to positive social change. In the 21st century, a movement that identifies as progressive is "a social or political movement that aims to represent the interests of ordinary people through political change and the support of government actions". `,
    imageUrl: triangleCircle,
  },
  {
    title: `Neutralism`,
    content: `Centrism is a political outlook or position that involves acceptance and/or support of a balance of social equality and a degree of social hierarchy, while opposing political changes which would result in a significant shift of society strongly to either the left or the right.

    Both centre-left and centre-right politics involve a general association with centrism that is combined with leaning somewhat to their respective sides of the left–right political spectrum. Various political ideologies, such as Christian democracy and social (or modern) liberalism, can be classified as centrist ones, as can the Third Way, a modern political movement that attempts to reconcile right-wing and left-wing politics by advocating for a synthesis of centre-right economic platforms with some centre-left social policies. `,
    imageUrl: ladyJustice,
  },
  {
    title: `Fundamentalism`,
    content: `Fundamentalism usually has a religious connotation that indicates unwavering attachment to a set of irreducible beliefs. However, fundamentalism has come to be applied to a tendency among certain groups – mainly, although not exclusively, in religion – that is characterized by a markedly strict literalism as it is applied to certain specific scriptures, dogmas, or ideologies, and a strong sense of the importance of maintaining ingroup and outgroup distinctions, leading to an emphasis on purity and the desire to return to a previous ideal from which advocates believe members have strayed. Rejection of diversity of opinion as applied to these established "fundamentals" and their accepted interpretation within the group often results from this tendency.

    Depending upon the context, the label "fundamentalism" can be a pejorative rather than a neutral characterization, similar to the ways that calling political perspectives "right-wing" or "left-wing" can have negative connotations. `,
    imageUrl: crown,
  },
  {
    title: `Socialism`,
    content: `Socialism is a political, social, and economic philosophy encompassing a range of economic and social systems characterised by social ownership of the means of production. It includes the political theories and movements associated with such systems. Social ownership can be public, collective, cooperative, or of equity. While no single definition encapsulates the many types of socialism, social ownership is the one common element. The types of socialism vary based on the role of markets and planning in resource allocation, on the structure of management in organizations, and socialists disagree on whether government, particularly existing government, is the correct vehicle for change.

    Socialist systems are divided into non-market and market forms. Non-market socialism substitutes factor markets and money with integrated economic planning and engineering or technical criteria based on calculation performed in-kind, thereby producing a different economic mechanism that functions according to different economic laws and dynamics than those of capitalism. A non-market socialist system eliminates the inefficiencies and crises traditionally associated with capital accumulation and the profit system in capitalism. The socialist calculation debate, originated by the economic calculation problem, concerns the feasibility and methods of resource allocation for a planned socialist system. By contrast, market socialism retains the use of monetary prices, factor markets and in some cases the profit motive, with respect to the operation of socially owned enterprises and the allocation of capital goods between them. Profits generated by these firms would be controlled directly by the workforce of each firm or accrue to society at large in the form of a social dividend. Anarchism and libertarian socialism oppose the use of the state as a means to establish socialism, favouring decentralisation above all, whether to establish non-market socialism or market socialism.
    
    Socialist politics has been both internationalist and nationalist in orientation; organised through political parties and opposed to party politics; at times overlapping with trade unions and at other times independent and critical of them; and present in both industrialised and developing nations. Social democracy originated within the socialist movement, supporting economic and social interventions to promote social justice. While nominally retaining socialism as a long-term goal, since the post-war period it has come to embrace a Keynesian mixed economy within a predominantly developed capitalist market economy and liberal democratic polity that expands state intervention to include income redistribution, regulation and a welfare state. Economic democracy proposes a sort of market socialism, with more democratic control of companies, currencies, investments and natural resources.
    
    The socialist political movement includes a set of political philosophies that originated in the revolutionary movements of the mid-to-late 18th century and out of concern for the social problems that were associated with capitalism. By the late 19th century, after the work of Karl Marx and his collaborator Friedrich Engels, socialism had come to signify opposition to capitalism and advocacy for a post-capitalist system based on some form of social ownership of the means of production. By the 1920s, communism and social democracy had become the two dominant political tendencies within the international socialist movement, with socialism itself becoming the most influential secular movement of the 20th century. Socialist parties and ideas remain a political force with varying degrees of power and influence on all continents, heading national governments in many countries around the world. Today, many socialists have also adopted the causes of other social movements such as environmentalism, feminism and progressivism.
    
    While the emergence of the Soviet Union as the world's first nominally socialist state led to socialism's widespread association with the Soviet economic model, some economists and intellectuals argued that in practice the model functioned as a form of state capitalism or a non-planned administrative or command economy. Academics, political commentators and other scholars sometimes refer to Western Bloc countries which have been democratically governed by socialist parties such as Britain, France, Sweden and Western social-democracies in general as democratic socialist.
    `,
    imageUrl: fist,
  },
  {
    title: `Reinvigoration`,
    content: `Reform is the improvement or amendment of what is wrong, corrupt, unsatisfactory, etc. The use of the word in this way emerges in the late 18th century and is believed to originate from Christopher Wyvill's Association movement which identified “Parliamentary Reform” as its primary aim. Reform is generally regarded as antithetical to revolution.

    Developing countries may carry out a wide range of reforms to improve their living standards, often with support from international financial institutions and aid agencies. This can include reforms to macroeconomic policy, the civil service, and public financial management.
    
    In the United States, rotation in office or term limits would, by contrast, be more revolutionary, in altering basic political connections between incumbents and constituents. `,
    imageUrl: pheonix,
  },
  {
    title: `Nationalism`,
    content: `Nationalism is an idea and movement that holds that the nation should be congruent with the state. As a movement, nationalism tends to promote the interests of a particular nation (as in a group of people), especially with the aim of gaining and maintaining the nation's sovereignty (self-governance) over its homeland. Nationalism holds that each nation should govern itself, free from outside interference (self-determination), that a nation is a natural and ideal basis for a polity and that the nation is the only rightful source of political power (popular sovereignty). It further aims to build and maintain a single national identity, based on shared social characteristics of culture, ethnicity, geographic location, language, politics (or the government), religion, traditions and belief in a shared singular history, and to promote national unity or solidarity. Nationalism seeks to preserve and foster a nation's traditional cultures and cultural revivals have been associated with nationalist movements. It also encourages pride in national achievements and is closely linked to patriotism. Nationalism can be combined with diverse political goals and ideologies such as conservatism (national conservatism) or socialism (left-wing nationalism).

    Throughout history, people have had an attachment to their kin group and traditions, territorial authorities and their homeland, but nationalism did not become a widely recognized concept until the end of the 18th century. There are three paradigms for understanding the origins and basis of nationalism. Primordialism (perennialism) proposes that there have always been nations and that nationalism is a natural phenomenon. Ethnosymbolism explains nationalism as a dynamic, evolutionary phenomenon and stresses the importance of symbols, myths and traditions in the development of nations and nationalism. Modernization theory proposes that nationalism is a recent social phenomenon that needs the socio-economic structures of modern society to exist.
    
    There are various definitions of a "nation" which leads to different types of nationalism. Ethnic nationalism defines the nation in terms of shared ethnicity, heritage and culture while civic nationalism defines the nation in terms of shared citizenship, values and institutions, and is linked to constitutional patriotism. The adoption of national identity in terms of historical development has often been a response by influential groups unsatisfied with traditional identities due to mismatch between their defined social order and the experience of that social order by its members, resulting in an anomie that nationalists seek to resolve. This anomie results in a society reinterpreting identity, retaining elements deemed acceptable and removing elements deemed unacceptable, to create a unified community. This development may be the result of internal structural issues or the result of resentment by an existing group or groups towards other communities, especially foreign powers that are (or are deemed to be) controlling them. National symbols and flags, national anthems, national languages, national myths and other symbols of national identity are highly important in nationalism.
    
    In practice, nationalism can be seen as positive or negative depending on context and individual outlook. Nationalism has been an important driver in independence movements such as the Greek Revolution, the Irish Revolution, the Zionist movement that created modern Israel and the dissolution of the Soviet Union. Radical nationalism combined with racial hatred was also a key factor in the Holocaust perpetrated by Nazi Germany. Nationalism was an important driver of the controversial annexation of Crimea by Russia.`,
    imageUrl: trident,
  },
  {
    title: `Divine Conservatism`,
    content: `
    Theocracy is a form of government in which a deity of some type is recognized as the supreme ruling authority, giving divine guidance to human intermediaries that manage the day-to-day affairs of the government.
    
    The Imperial cult of ancient Rome identified Roman emperors and some members of their families with the divinely sanctioned authority (auctoritas) of the Roman State. The official offer of cultus to a living emperor acknowledged his office and rule as divinely approved and constitutional: his Principate should therefore demonstrate pious respect for traditional Republican deities and mores.
    Contents.`,
    imageUrl: bible,
  },
  {
    title: `Activism`,
    content: `Activism consists of efforts to promote, impede, direct, or intervene in social, political, economic, legal, or environmental reform with the desire to make changes in society toward a perceived greater good. Forms of activism range from mandate building in the community (including writing letters to newspapers), petitioning elected officials, running or contributing to a political campaign, preferential patronage (or boycott) of businesses, and demonstrative forms of activism like rallies, street marches, strikes, sit-ins, or hunger strikes.

    Activism may be performed on a day-to-day basis in a wide variety of ways, including through the creation of art (artivism), computer hacking (hacktivism), or simply in how one chooses to spend their money (economic activism). For example, the refusal to buy clothes or other merchandise from a company as a protest against the exploitation of workers by that company could be considered an expression of activism. However, the most highly visible and impactful activism often comes in the form of collective action, in which numerous individuals coordinate an act of protest together in order to make a bigger impact. Collective action that is purposeful, organized, and sustained over a period of time becomes known as a social movement.
    
    Historically, activists have used literature, including pamphlets, tracts, and books to disseminate or propagate their messages and attempt to persuade their readers of the justice of their cause. Research has now begun to explore how contemporary activist groups use social media to facilitate civic engagement and collective action combining politics with technology.`,
    imageUrl: pidgeon,
  },
  {
    title: `Statism`,
    content: `In political science, statism is the doctrine that the political authority of the state is legitimate to some degree. This may include economic and social policy, especially in regard to taxation and the means of production.

    While in use since the 1850s, the term statism gained significant usage in American political discourse throughout the 1930s and 1940s. Opposition to statism is termed anti-statism or anarchism. The latter is characterized by a complete rejection of all hierarchical rulership. `,
    imageUrl: lion,
  },
  {
    title: `Technocratism`,
    content: `Technocracy is a system of government in which a decision-maker or makers are elected by the population or appointed on the basis of their expertise in a given area of responsibility, particularly with regard to scientific or technical knowledge. This system explicitly contrasts with representative democracy, the notion that elected representatives should be the primary decision-makers in government, though it does not necessarily imply eliminating elected representatives. Decision-makers are selected on the basis of specialized knowledge and performance, rather than political affiliations or parliamentary skills.

    The term technocracy was originally used to signify the application of the scientific method to solving social problems. Concern could be given to sustainability within the resource base, instead of monetary profitability, so as to ensure continued operation of all social-industrial functions. In its most extreme sense technocracy is an entire government running as a technical or engineering problem and is mostly hypothetical. In more practical use, technocracy is any portion of a bureaucracy that is run by technologists. A government in which elected officials appoint experts and professionals to administer individual government functions and recommend legislation can be considered technocratic. Some uses of the word refer to a form of meritocracy, where the ablest are in charge, ostensibly without the influence of special interest groups. Critics have suggested that a "technocratic divide" challenges more participatory models of democracy, describing these divides as "efficacy gaps that persist between governing bodies employing technocratic principles and members of the general public aiming to contribute to government decision making".`,
    imageUrl: owl,
  }
];

const InitiativesPage = () => {
  const [end, setEnd] = useState("");
  const [initiatives, setInitiatives] = useState<Array<number>>();
  const [isEnd, SetIsEnd] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  React.useEffect(() => {
    getEndDate();
    getInitiatives()
  }, [])
  interface initiativeAPI {
    initiative_type: number
    // datetime of election start
    election: string
    policy_type_weights: []
  }
  const getInitiatives = async () => {
    const initiativeUrl = "http://localhost:8000/api/v1/initiative/"
    try {
      axios
        .get(initiativeUrl)
        .then(res => {
          console.log(res.data)
          let initiativeArr = res.data.map((i: any) =>
            i['initiative_type']
          )
          setInitiatives(initiativeArr)
        })
    } catch (error) {
      setErrorMsg('An error has occured, please try again.')
    }
  }
  const mapper = () => {
    let cardArr = []
    for (let initiative in initiatives) {
      let mapId = INITIATIVE_MAP[initiative]
      let res = INITIATIVES.filter(k => k.title == mapId)[0]
      cardArr.push(res)
    }
    return cardArr
  }

  async function getEndDate() {
    
    const voteUrl = "http://localhost:8000/api/v1/election/"
    try {
      let request = await axios.get(voteUrl)
      if (request.data.length > 0 && request.data[0]['is_active']) {
        var date = new Date(request.data[0]['election_end']);
        const options = {
          day: "numeric",
          month: "long",
          year: "numeric",
          hour: "numeric",
          minute: "numeric",
          timeZoneName: 'short',
        };
        SetIsEnd(true);
        setEnd(date.toLocaleDateString('en-AU', options));
      } else {
        SetIsEnd(false);
      }
    } catch (error) {
      setErrorMsg('An error has occured, please try again.')
    }
  }

  return (
    <>
      {Banner({ title: "Initiatives", subtitle: end, quote: "Create with the heart; build with the mind", author: "Criss Jami" })}
      <Box h='2rem' gridColumn='4/12' />
      {isEnd && (
        <PageTitle
          title='Iniatiatives'
          subtitle={`Current Voting stage ends: ${end}`}
        />
      )}
      {!isEnd && (
        <PageTitle
          title='Iniatiatives'
          subtitle={`There is no active vote right now.`}
        />
      )}
      
      <Box h='4rem' gridColumn='4/12' />
      {assignCards(INITIATIVES)}

      <Popups type="error" message={errorMsg}/>
    </>)
};

export default InitiativesPage;
